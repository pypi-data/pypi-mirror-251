//========================================================================
// GLFW 3.3 Wayland - www.glfw.org
//------------------------------------------------------------------------
// Copyright (c) 2014 Jonas Ådahl <jadahl@gmail.com>
//
// This software is provided 'as-is', without any express or implied
// warranty. In no event will the authors be held liable for any damages
// arising from the use of this software.
//
// Permission is granted to anyone to use this software for any purpose,
// including commercial applications, and to alter it and redistribute it
// freely, subject to the following restrictions:
//
// 1. The origin of this software must not be misrepresented; you must not
//    claim that you wrote the original software. If you use this software
//    in a product, an acknowledgment in the product documentation would
//    be appreciated but is not required.
//
// 2. Altered source versions must be plainly marked as such, and must not
//    be misrepresented as being the original software.
//
// 3. This notice may not be removed or altered from any source
//    distribution.
//
//========================================================================
// It is fine to use C99 in this file because it will not be built with VS
//========================================================================

#define _GNU_SOURCE

#include "internal.h"

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/timerfd.h>
#include <poll.h>
#include <signal.h>
#include <time.h>

#define GLFW_BORDER_SIZE    4
#define GLFW_CAPTION_HEIGHT 24

static int createTmpfileCloexec(char* tmpname)
{
    int fd;

    fd = mkostemp(tmpname, O_CLOEXEC);
    if (fd >= 0)
        unlink(tmpname);

    return fd;
}

/*
 * Create a new, unique, anonymous file of the given size, and
 * return the file descriptor for it. The file descriptor is set
 * CLOEXEC. The file is immediately suitable for mmap()'ing
 * the given size at offset zero.
 *
 * The file should not have a permanent backing store like a disk,
 * but may have if XDG_RUNTIME_DIR is not properly implemented in OS.
 *
 * The file name is deleted from the file system.
 *
 * The file is suitable for buffer sharing between processes by
 * transmitting the file descriptor over Unix sockets using the
 * SCM_RIGHTS methods.
 *
 * posix_fallocate() is used to guarantee that disk space is available
 * for the file at the given size. If disk space is insufficient, errno
 * is set to ENOSPC. If posix_fallocate() is not supported, program may
 * receive SIGBUS on accessing mmap()'ed file contents instead.
 */
static int createAnonymousFile(off_t size)
{
    static const char template[] = "/glfw-shared-XXXXXX";
    const char* path;
    char* name;
    int fd;
    int ret;

#ifdef HAVE_MEMFD_CREATE
    fd = memfd_create("glfw-shared", MFD_CLOEXEC | MFD_ALLOW_SEALING);
    if (fd >= 0)
    {
        // We can add this seal before calling posix_fallocate(), as the file
        // is currently zero-sized anyway.
        //
        // There is also no need to check for the return value, we couldn’t do
        // anything with it anyway.
        fcntl(fd, F_ADD_SEALS, F_SEAL_SHRINK | F_SEAL_SEAL);
    }
    else
#elif defined(SHM_ANON)
    fd = shm_open(SHM_ANON, O_RDWR | O_CLOEXEC, 0600);
    if (fd < 0)
#endif
    {
        path = getenv("XDG_RUNTIME_DIR");
        if (!path)
        {
            errno = ENOENT;
            return -1;
        }

        name = calloc(strlen(path) + sizeof(template), 1);
        strcpy(name, path);
        strcat(name, template);

        fd = createTmpfileCloexec(name);
        free(name);
        if (fd < 0)
            return -1;
    }

#if defined(SHM_ANON)
    // posix_fallocate does not work on SHM descriptors
    ret = ftruncate(fd, size);
#else
    ret = posix_fallocate(fd, 0, size);
#endif
    if (ret != 0)
    {
        close(fd);
        errno = ret;
        return -1;
    }
    return fd;
}

static struct wl_buffer* createShmBuffer(const GLFWimage* image)
{
    const int stride = image->width * 4;
    const int length = image->width * image->height * 4;

    const int fd = createAnonymousFile(length);
    if (fd < 0)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to create buffer file of size %d: %s",
                        length, strerror(errno));
        return NULL;
    }

    void* data = mmap(NULL, length, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (data == MAP_FAILED)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to map file: %s", strerror(errno));
        close(fd);
        return NULL;
    }

    struct wl_shm_pool* pool = wl_shm_create_pool(_glfw.wl.shm, fd, length);

    close(fd);

    unsigned char* source = (unsigned char*) image->pixels;
    unsigned char* target = data;
    for (int i = 0;  i < image->width * image->height;  i++, source += 4)
    {
        unsigned int alpha = source[3];

        *target++ = (unsigned char) ((source[2] * alpha) / 255);
        *target++ = (unsigned char) ((source[1] * alpha) / 255);
        *target++ = (unsigned char) ((source[0] * alpha) / 255);
        *target++ = (unsigned char) alpha;
    }

    struct wl_buffer* buffer =
        wl_shm_pool_create_buffer(pool, 0,
                                  image->width,
                                  image->height,
                                  stride, WL_SHM_FORMAT_ARGB8888);
    munmap(data, length);
    wl_shm_pool_destroy(pool);

    return buffer;
}

// Wait for data to arrive on any of the specified file descriptors
//
static GLFWbool waitForData(struct pollfd* fds, nfds_t count, double* timeout)
{
    for (;;)
    {
        if (timeout)
        {
            const uint64_t base = _glfwPlatformGetTimerValue();

#if defined(__linux__) || defined(__FreeBSD__) || defined(__OpenBSD__) || defined(__CYGWIN__)
            const time_t seconds = (time_t) *timeout;
            const long nanoseconds = (long) ((*timeout - seconds) * 1e9);
            const struct timespec ts = { seconds, nanoseconds };
            const int result = ppoll(fds, count, &ts, NULL);
#elif defined(__NetBSD__)
            const time_t seconds = (time_t) *timeout;
            const long nanoseconds = (long) ((*timeout - seconds) * 1e9);
            const struct timespec ts = { seconds, nanoseconds };
            const int result = pollts(fds, count, &ts, NULL);
#else
            const int milliseconds = (int) (*timeout * 1e3);
            const int result = poll(fds, count, milliseconds);
#endif
            const int error = errno; // clock_gettime may overwrite our error

            *timeout -= (_glfwPlatformGetTimerValue() - base) /
                (double) _glfwPlatformGetTimerFrequency();

            if (result > 0)
                return GLFW_TRUE;
            else if (result == -1 && error != EINTR && error != EAGAIN)
                return GLFW_FALSE;
            else if (*timeout <= 0.0)
                return GLFW_FALSE;
        }
        else
        {
            const int result = poll(fds, count, -1);
            if (result > 0)
                return GLFW_TRUE;
            else if (result == -1 && errno != EINTR && errno != EAGAIN)
                return GLFW_FALSE;
        }
    }
}

static void createFallbackDecoration(_GLFWwindow* window,
                                     _GLFWdecorationWayland* decoration,
                                     struct wl_surface* parent,
                                     struct wl_buffer* buffer,
                                     int x, int y,
                                     int width, int height)
{
    decoration->surface = wl_compositor_create_surface(_glfw.wl.compositor);
    wl_surface_set_user_data(decoration->surface, window);
    wl_proxy_set_tag((struct wl_proxy*) decoration->surface, &_glfw.wl.tag);
    decoration->subsurface =
        wl_subcompositor_get_subsurface(_glfw.wl.subcompositor,
                                        decoration->surface, parent);
    wl_subsurface_set_position(decoration->subsurface, x, y);
    decoration->viewport = wp_viewporter_get_viewport(_glfw.wl.viewporter,
                                                      decoration->surface);
    wp_viewport_set_destination(decoration->viewport, width, height);
    wl_surface_attach(decoration->surface, buffer, 0, 0);

    struct wl_region* region = wl_compositor_create_region(_glfw.wl.compositor);
    wl_region_add(region, 0, 0, width, height);
    wl_surface_set_opaque_region(decoration->surface, region);
    wl_surface_commit(decoration->surface);
    wl_region_destroy(region);
}

static void createFallbackDecorations(_GLFWwindow* window)
{
    unsigned char data[] = { 224, 224, 224, 255 };
    const GLFWimage image = { 1, 1, data };

    if (!_glfw.wl.viewporter)
        return;

    if (!window->wl.decorations.buffer)
        window->wl.decorations.buffer = createShmBuffer(&image);
    if (!window->wl.decorations.buffer)
        return;

    createFallbackDecoration(window, &window->wl.decorations.top, window->wl.surface,
                             window->wl.decorations.buffer,
                             0, -GLFW_CAPTION_HEIGHT,
                             window->wl.width, GLFW_CAPTION_HEIGHT);
    createFallbackDecoration(window, &window->wl.decorations.left, window->wl.surface,
                             window->wl.decorations.buffer,
                             -GLFW_BORDER_SIZE, -GLFW_CAPTION_HEIGHT,
                             GLFW_BORDER_SIZE, window->wl.height + GLFW_CAPTION_HEIGHT);
    createFallbackDecoration(window, &window->wl.decorations.right, window->wl.surface,
                             window->wl.decorations.buffer,
                             window->wl.width, -GLFW_CAPTION_HEIGHT,
                             GLFW_BORDER_SIZE, window->wl.height + GLFW_CAPTION_HEIGHT);
    createFallbackDecoration(window, &window->wl.decorations.bottom, window->wl.surface,
                             window->wl.decorations.buffer,
                             -GLFW_BORDER_SIZE, window->wl.height,
                             window->wl.width + GLFW_BORDER_SIZE * 2, GLFW_BORDER_SIZE);
}

static void destroyFallbackDecoration(_GLFWdecorationWayland* decoration)
{
    if (decoration->subsurface)
        wl_subsurface_destroy(decoration->subsurface);
    if (decoration->surface)
        wl_surface_destroy(decoration->surface);
    if (decoration->viewport)
        wp_viewport_destroy(decoration->viewport);
    decoration->surface = NULL;
    decoration->subsurface = NULL;
    decoration->viewport = NULL;
}

static void destroyFallbackDecorations(_GLFWwindow* window)
{
    destroyFallbackDecoration(&window->wl.decorations.top);
    destroyFallbackDecoration(&window->wl.decorations.left);
    destroyFallbackDecoration(&window->wl.decorations.right);
    destroyFallbackDecoration(&window->wl.decorations.bottom);
}

static void xdgDecorationHandleConfigure(void* userData,
                                         struct zxdg_toplevel_decoration_v1* decoration,
                                         uint32_t mode)
{
    _GLFWwindow* window = userData;

    window->wl.xdg.decorationMode = mode;

    if (mode == ZXDG_TOPLEVEL_DECORATION_V1_MODE_CLIENT_SIDE)
    {
        if (window->decorated && !window->monitor)
            createFallbackDecorations(window);
    }
    else
        destroyFallbackDecorations(window);
}

static const struct zxdg_toplevel_decoration_v1_listener xdgDecorationListener =
{
    xdgDecorationHandleConfigure,
};

// Makes the surface considered as XRGB instead of ARGB.
static void setContentAreaOpaque(_GLFWwindow* window)
{
    struct wl_region* region;

    region = wl_compositor_create_region(_glfw.wl.compositor);
    if (!region)
        return;

    wl_region_add(region, 0, 0, window->wl.width, window->wl.height);
    wl_surface_set_opaque_region(window->wl.surface, region);
    wl_region_destroy(region);
}


static void resizeWindow(_GLFWwindow* window)
{
    int scale = window->wl.contentScale;
    int scaledWidth = window->wl.width * scale;
    int scaledHeight = window->wl.height * scale;

    if (window->wl.egl.window)
        wl_egl_window_resize(window->wl.egl.window, scaledWidth, scaledHeight, 0, 0);
    if (!window->wl.transparent)
        setContentAreaOpaque(window);
    _glfwInputFramebufferSize(window, scaledWidth, scaledHeight);

    if (!window->wl.decorations.top.surface)
        return;

    wp_viewport_set_destination(window->wl.decorations.top.viewport,
                                window->wl.width, GLFW_CAPTION_HEIGHT);
    wl_surface_commit(window->wl.decorations.top.surface);

    wp_viewport_set_destination(window->wl.decorations.left.viewport,
                                GLFW_BORDER_SIZE, window->wl.height + GLFW_CAPTION_HEIGHT);
    wl_surface_commit(window->wl.decorations.left.surface);

    wl_subsurface_set_position(window->wl.decorations.right.subsurface,
                               window->wl.width, -GLFW_CAPTION_HEIGHT);
    wp_viewport_set_destination(window->wl.decorations.right.viewport,
                                GLFW_BORDER_SIZE, window->wl.height + GLFW_CAPTION_HEIGHT);
    wl_surface_commit(window->wl.decorations.right.surface);

    wl_subsurface_set_position(window->wl.decorations.bottom.subsurface,
                               -GLFW_BORDER_SIZE, window->wl.height);
    wp_viewport_set_destination(window->wl.decorations.bottom.viewport,
                                window->wl.width + GLFW_BORDER_SIZE * 2, GLFW_BORDER_SIZE);
    wl_surface_commit(window->wl.decorations.bottom.surface);
}

void _glfwUpdateContentScaleWayland(_GLFWwindow* window)
{
    if (wl_compositor_get_version(_glfw.wl.compositor) <
        WL_SURFACE_SET_BUFFER_SCALE_SINCE_VERSION)
    {
        return;
    }

    // Get the scale factor from the highest scale monitor.
    int maxScale = 1;

    for (int i = 0; i < window->wl.scaleCount; i++)
        maxScale = _glfw_max(window->wl.scales[i].factor, maxScale);

    // Only change the framebuffer size if the scale changed.
    if (window->wl.contentScale != maxScale)
    {
        window->wl.contentScale = maxScale;
        wl_surface_set_buffer_scale(window->wl.surface, maxScale);
        _glfwInputWindowContentScale(window, maxScale, maxScale);
        resizeWindow(window);

        if (window->wl.visible)
            _glfwInputWindowDamage(window);
    }
}

static void surfaceHandleEnter(void* userData,
                               struct wl_surface* surface,
                               struct wl_output* output)
{
    if (wl_proxy_get_tag((struct wl_proxy*) output) != &_glfw.wl.tag)
        return;

    _GLFWwindow* window = userData;
    _GLFWmonitor* monitor = wl_output_get_user_data(output);
    if (!window || !monitor)
        return;

    if (window->wl.scaleCount + 1 > window->wl.scaleSize)
    {
        window->wl.scaleSize++;
        window->wl.scales =
            realloc(window->wl.scales,
                    window->wl.scaleSize * sizeof(_GLFWscaleWayland));
    }

    window->wl.scaleCount++;
    window->wl.scales[window->wl.scaleCount - 1].factor = monitor->wl.contentScale;
    window->wl.scales[window->wl.scaleCount - 1].output = output;

    _glfwUpdateContentScaleWayland(window);
}

static void surfaceHandleLeave(void* userData,
                               struct wl_surface* surface,
                               struct wl_output* output)
{
    if (wl_proxy_get_tag((struct wl_proxy*) output) != &_glfw.wl.tag)
        return;

    _GLFWwindow* window = userData;

    for (int i = 0; i < window->wl.scaleCount; i++)
    {
        if (window->wl.scales[i].output == output)
        {
            window->wl.scales[i] = window->wl.scales[window->wl.scaleCount - 1];
            window->wl.scaleCount--;
            break;
        }
    }

    _glfwUpdateContentScaleWayland(window);
}

static const struct wl_surface_listener surfaceListener =
{
    surfaceHandleEnter,
    surfaceHandleLeave
};

static void setIdleInhibitor(_GLFWwindow* window, GLFWbool enable)
{
    if (enable && !window->wl.idleInhibitor && _glfw.wl.idleInhibitManager)
    {
        window->wl.idleInhibitor =
            zwp_idle_inhibit_manager_v1_create_inhibitor(
                _glfw.wl.idleInhibitManager, window->wl.surface);
        if (!window->wl.idleInhibitor)
            _glfwInputError(GLFW_PLATFORM_ERROR,
                            "Wayland: Failed to create idle inhibitor");
    }
    else if (!enable && window->wl.idleInhibitor)
    {
        zwp_idle_inhibitor_v1_destroy(window->wl.idleInhibitor);
        window->wl.idleInhibitor = NULL;
    }
}

// Make the specified window and its video mode active on its monitor
//
static void acquireMonitor(_GLFWwindow* window)
{
    if (window->wl.libdecor.frame)
    {
        libdecor_frame_set_fullscreen(window->wl.libdecor.frame,
                                      window->monitor->wl.output);
    }
    else if (window->wl.xdg.toplevel)
    {
        xdg_toplevel_set_fullscreen(window->wl.xdg.toplevel,
                                    window->monitor->wl.output);
    }

    setIdleInhibitor(window, GLFW_TRUE);

    if (window->wl.decorations.top.surface)
        destroyFallbackDecorations(window);
}

// Remove the window and restore the original video mode
//
static void releaseMonitor(_GLFWwindow* window)
{
    if (window->wl.libdecor.frame)
        libdecor_frame_unset_fullscreen(window->wl.libdecor.frame);
    else if (window->wl.xdg.toplevel)
        xdg_toplevel_unset_fullscreen(window->wl.xdg.toplevel);

    setIdleInhibitor(window, GLFW_FALSE);

    if (!window->wl.libdecor.frame &&
        window->wl.xdg.decorationMode != ZXDG_TOPLEVEL_DECORATION_V1_MODE_SERVER_SIDE)
    {
        if (window->decorated)
            createFallbackDecorations(window);
    }
}

static void xdgToplevelHandleConfigure(void* userData,
                                       struct xdg_toplevel* toplevel,
                                       int32_t width,
                                       int32_t height,
                                       struct wl_array* states)
{
    _GLFWwindow* window = userData;
    uint32_t* state;

    window->wl.pending.activated  = GLFW_FALSE;
    window->wl.pending.maximized  = GLFW_FALSE;
    window->wl.pending.fullscreen = GLFW_FALSE;

    wl_array_for_each(state, states)
    {
        switch (*state)
        {
            case XDG_TOPLEVEL_STATE_MAXIMIZED:
                window->wl.pending.maximized = GLFW_TRUE;
                break;
            case XDG_TOPLEVEL_STATE_FULLSCREEN:
                window->wl.pending.fullscreen = GLFW_TRUE;
                break;
            case XDG_TOPLEVEL_STATE_RESIZING:
                break;
            case XDG_TOPLEVEL_STATE_ACTIVATED:
                window->wl.pending.activated = GLFW_TRUE;
                break;
        }
    }

    if (width && height)
    {
        if (window->wl.decorations.top.surface)
        {
            window->wl.pending.width  = _glfw_max(0, width - GLFW_BORDER_SIZE * 2);
            window->wl.pending.height =
                _glfw_max(0, height - GLFW_BORDER_SIZE - GLFW_CAPTION_HEIGHT);
        }
        else
        {
            window->wl.pending.width  = width;
            window->wl.pending.height = height;
        }
    }
    else
    {
        window->wl.pending.width  = window->wl.width;
        window->wl.pending.height = window->wl.height;
    }
}

static void xdgToplevelHandleClose(void* userData,
                                   struct xdg_toplevel* toplevel)
{
    _GLFWwindow* window = userData;
    _glfwInputWindowCloseRequest(window);
}

static const struct xdg_toplevel_listener xdgToplevelListener =
{
    xdgToplevelHandleConfigure,
    xdgToplevelHandleClose
};

static void xdgSurfaceHandleConfigure(void* userData,
                                      struct xdg_surface* surface,
                                      uint32_t serial)
{
    _GLFWwindow* window = userData;

    xdg_surface_ack_configure(surface, serial);

    if (window->wl.activated != window->wl.pending.activated)
    {
        window->wl.activated = window->wl.pending.activated;
        if (!window->wl.activated)
        {
            if (window->monitor && window->autoIconify)
                xdg_toplevel_set_minimized(window->wl.xdg.toplevel);
        }
    }

    if (window->wl.maximized != window->wl.pending.maximized)
    {
        window->wl.maximized = window->wl.pending.maximized;
        _glfwInputWindowMaximize(window, window->wl.maximized);
    }

    window->wl.fullscreen = window->wl.pending.fullscreen;

    int width  = window->wl.pending.width;
    int height = window->wl.pending.height;

    if (!window->wl.maximized && !window->wl.fullscreen)
    {
        if (window->numer != GLFW_DONT_CARE && window->denom != GLFW_DONT_CARE)
        {
            const float aspectRatio = (float) width / (float) height;
            const float targetRatio = (float) window->numer / (float) window->denom;
            if (aspectRatio < targetRatio)
                height = width / targetRatio;
            else if (aspectRatio > targetRatio)
                width = height * targetRatio;
        }
    }

    if (width != window->wl.width || height != window->wl.height)
    {
        window->wl.width = width;
        window->wl.height = height;
        resizeWindow(window);

        _glfwInputWindowSize(window, width, height);

        if (window->wl.visible)
            _glfwInputWindowDamage(window);
    }

    if (!window->wl.visible)
    {
        // Allow the window to be mapped only if it either has no XDG
        // decorations or they have already received a configure event
        if (!window->wl.xdg.decoration || window->wl.xdg.decorationMode)
        {
            window->wl.visible = GLFW_TRUE;
            _glfwInputWindowDamage(window);
        }
    }
}

static const struct xdg_surface_listener xdgSurfaceListener =
{
    xdgSurfaceHandleConfigure
};

void libdecorFrameHandleConfigure(struct libdecor_frame* frame,
                                  struct libdecor_configuration* config,
                                  void* userData)
{
    _GLFWwindow* window = userData;
    int width, height;

    enum libdecor_window_state windowState;
    GLFWbool fullscreen, activated, maximized;

    if (libdecor_configuration_get_window_state(config, &windowState))
    {
        fullscreen = (windowState & LIBDECOR_WINDOW_STATE_FULLSCREEN) != 0;
        activated = (windowState & LIBDECOR_WINDOW_STATE_ACTIVE) != 0;
        maximized = (windowState & LIBDECOR_WINDOW_STATE_MAXIMIZED) != 0;
    }
    else
    {
        fullscreen = window->wl.fullscreen;
        activated = window->wl.activated;
        maximized = window->wl.maximized;
    }

    if (!libdecor_configuration_get_content_size(config, frame, &width, &height))
    {
        width = window->wl.width;
        height = window->wl.height;
    }

    if (!maximized && !fullscreen)
    {
        if (window->numer != GLFW_DONT_CARE && window->denom != GLFW_DONT_CARE)
        {
            const float aspectRatio = (float) width / (float) height;
            const float targetRatio = (float) window->numer / (float) window->denom;
            if (aspectRatio < targetRatio)
                height = width / targetRatio;
            else if (aspectRatio > targetRatio)
                width = height * targetRatio;
        }
    }

    struct libdecor_state* frameState = libdecor_state_new(width, height);
    libdecor_frame_commit(frame, frameState, config);
    libdecor_state_free(frameState);

    if (window->wl.activated != activated)
    {
        window->wl.activated = activated;
        if (!window->wl.activated)
        {
            if (window->monitor && window->autoIconify)
                libdecor_frame_set_minimized(window->wl.libdecor.frame);
        }
    }

    if (window->wl.maximized != maximized)
    {
        window->wl.maximized = maximized;
        _glfwInputWindowMaximize(window, window->wl.maximized);
    }

    window->wl.fullscreen = fullscreen;

    GLFWbool damaged = GLFW_FALSE;

    if (!window->wl.visible)
    {
        window->wl.visible = GLFW_TRUE;
        damaged = GLFW_TRUE;
    }

    if (width != window->wl.width || height != window->wl.height)
    {
        window->wl.width = width;
        window->wl.height = height;
        resizeWindow(window);

        _glfwInputWindowSize(window, width, height);
        damaged = GLFW_TRUE;
    }

    if (damaged)
        _glfwInputWindowDamage(window);
    else
        wl_surface_commit(window->wl.surface);
}

void libdecorFrameHandleClose(struct libdecor_frame* frame, void* userData)
{
    _GLFWwindow* window = userData;
    _glfwInputWindowCloseRequest(window);
}

void libdecorFrameHandleCommit(struct libdecor_frame* frame, void* userData)
{
    _GLFWwindow* window = userData;
    wl_surface_commit(window->wl.surface);
}

void libdecorFrameHandleDismissPopup(struct libdecor_frame* frame,
                                     const char* seatName,
                                     void* userData)
{
}

static const struct libdecor_frame_interface libdecorFrameInterface =
{
    libdecorFrameHandleConfigure,
    libdecorFrameHandleClose,
    libdecorFrameHandleCommit,
    libdecorFrameHandleDismissPopup
};

static GLFWbool createLibdecorFrame(_GLFWwindow* window)
{
    // Allow libdecor to finish initialization of itself and its plugin
    while (!_glfw.wl.libdecor.ready)
        _glfwPlatformWaitEvents();

    window->wl.libdecor.frame = libdecor_decorate(_glfw.wl.libdecor.context,
                                                  window->wl.surface,
                                                  &libdecorFrameInterface,
                                                  window);
    if (!window->wl.libdecor.frame)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to create libdecor frame");
        return GLFW_FALSE;
    }

    struct libdecor_state* frameState =
        libdecor_state_new(window->wl.width, window->wl.height);
    libdecor_frame_commit(window->wl.libdecor.frame, frameState, NULL);
    libdecor_state_free(frameState);

    if (strlen(window->wl.title))
        libdecor_frame_set_title(window->wl.libdecor.frame, window->wl.title);

    if (window->minwidth != GLFW_DONT_CARE &&
        window->minheight != GLFW_DONT_CARE)
    {
        libdecor_frame_set_min_content_size(window->wl.libdecor.frame,
                                            window->minwidth,
                                            window->minheight);
    }

    if (window->maxwidth != GLFW_DONT_CARE &&
        window->maxheight != GLFW_DONT_CARE)
    {
        libdecor_frame_set_max_content_size(window->wl.libdecor.frame,
                                            window->maxwidth,
                                            window->maxheight);
    }

    if (!window->resizable)
    {
        libdecor_frame_unset_capabilities(window->wl.libdecor.frame,
                                          LIBDECOR_ACTION_RESIZE);
    }

    if (window->monitor)
    {
        libdecor_frame_set_fullscreen(window->wl.libdecor.frame,
                                      window->monitor->wl.output);
        setIdleInhibitor(window, GLFW_TRUE);
    }
    else
    {
        if (window->wl.maximized)
            libdecor_frame_set_maximized(window->wl.libdecor.frame);

        if (!window->decorated)
            libdecor_frame_set_visibility(window->wl.libdecor.frame, false);

        setIdleInhibitor(window, GLFW_FALSE);
    }

    libdecor_frame_map(window->wl.libdecor.frame);
    wl_display_roundtrip(_glfw.wl.display);
    return GLFW_TRUE;
}

static GLFWbool createXdgShellObjects(_GLFWwindow* window)
{
    window->wl.xdg.surface = xdg_wm_base_get_xdg_surface(_glfw.wl.wmBase,
                                                         window->wl.surface);
    if (!window->wl.xdg.surface)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to create xdg-surface for window");
        return GLFW_FALSE;
    }

    xdg_surface_add_listener(window->wl.xdg.surface, &xdgSurfaceListener, window);

    window->wl.xdg.toplevel = xdg_surface_get_toplevel(window->wl.xdg.surface);
    if (!window->wl.xdg.toplevel)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to create xdg-toplevel for window");
        return GLFW_FALSE;
    }

    xdg_toplevel_add_listener(window->wl.xdg.toplevel, &xdgToplevelListener, window);

    if (window->wl.title)
        xdg_toplevel_set_title(window->wl.xdg.toplevel, window->wl.title);

    if (window->monitor)
    {
        xdg_toplevel_set_fullscreen(window->wl.xdg.toplevel, window->monitor->wl.output);
        setIdleInhibitor(window, GLFW_TRUE);
    }
    else
    {
        if (window->wl.maximized)
            xdg_toplevel_set_maximized(window->wl.xdg.toplevel);

        setIdleInhibitor(window, GLFW_FALSE);
    }

    if (_glfw.wl.decorationManager)
    {
        window->wl.xdg.decoration =
            zxdg_decoration_manager_v1_get_toplevel_decoration(
                _glfw.wl.decorationManager, window->wl.xdg.toplevel);
        zxdg_toplevel_decoration_v1_add_listener(window->wl.xdg.decoration,
                                                 &xdgDecorationListener,
                                                 window);

        uint32_t mode;

        if (window->decorated)
            mode = ZXDG_TOPLEVEL_DECORATION_V1_MODE_SERVER_SIDE;
        else
            mode = ZXDG_TOPLEVEL_DECORATION_V1_MODE_CLIENT_SIDE;

        zxdg_toplevel_decoration_v1_set_mode(window->wl.xdg.decoration, mode);
    }
    else
    {
        if (window->decorated && !window->monitor)
            createFallbackDecorations(window);
    }

    if (window->minwidth != GLFW_DONT_CARE && window->minheight != GLFW_DONT_CARE)
    {
        int minwidth  = window->minwidth;
        int minheight = window->minheight;

        if (window->wl.decorations.top.surface)
        {
            minwidth  += GLFW_BORDER_SIZE * 2;
            minheight += GLFW_CAPTION_HEIGHT + GLFW_BORDER_SIZE;
        }

        xdg_toplevel_set_min_size(window->wl.xdg.toplevel, minwidth, minheight);
    }

    if (window->maxwidth != GLFW_DONT_CARE && window->maxheight != GLFW_DONT_CARE)
    {
        int maxwidth  = window->maxwidth;
        int maxheight = window->maxheight;

        if (window->wl.decorations.top.surface)
        {
            maxwidth  += GLFW_BORDER_SIZE * 2;
            maxheight += GLFW_CAPTION_HEIGHT + GLFW_BORDER_SIZE;
        }

        xdg_toplevel_set_max_size(window->wl.xdg.toplevel, maxwidth, maxheight);
    }

    wl_surface_commit(window->wl.surface);
    wl_display_roundtrip(_glfw.wl.display);
    return GLFW_TRUE;
}

static GLFWbool createShellObjects(_GLFWwindow* window)
{
    if (_glfw.wl.libdecor.context)
    {
        if (createLibdecorFrame(window))
            return GLFW_TRUE;
    }

    return createXdgShellObjects(window);
}

static void destroyShellObjects(_GLFWwindow* window)
{
    destroyFallbackDecorations(window);

    if (window->wl.libdecor.frame)
        libdecor_frame_unref(window->wl.libdecor.frame);

    if (window->wl.xdg.decoration)
        zxdg_toplevel_decoration_v1_destroy(window->wl.xdg.decoration);

    if (window->wl.xdg.toplevel)
        xdg_toplevel_destroy(window->wl.xdg.toplevel);

    if (window->wl.xdg.surface)
        xdg_surface_destroy(window->wl.xdg.surface);

    window->wl.libdecor.frame = NULL;
    window->wl.xdg.decoration = NULL;
    window->wl.xdg.decorationMode = 0;
    window->wl.xdg.toplevel = NULL;
    window->wl.xdg.surface = NULL;
}

static GLFWbool createNativeSurface(_GLFWwindow* window,
                                    const _GLFWwndconfig* wndconfig,
                                    const _GLFWfbconfig* fbconfig)
{
    window->wl.surface = wl_compositor_create_surface(_glfw.wl.compositor);
    if (!window->wl.surface)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR, "Wayland: Failed to create window surface");
        return GLFW_FALSE;
    }

    wl_proxy_set_tag((struct wl_proxy*) window->wl.surface, &_glfw.wl.tag);
    wl_surface_add_listener(window->wl.surface,
                            &surfaceListener,
                            window);

    window->wl.width = wndconfig->width;
    window->wl.height = wndconfig->height;
    window->wl.contentScale = 1;
    window->wl.title = _glfw_strdup(wndconfig->title);

    window->wl.maximized = wndconfig->maximized;

    window->wl.transparent = fbconfig->transparent;
    if (!window->wl.transparent)
        setContentAreaOpaque(window);

    return GLFW_TRUE;
}

static void setCursorImage(_GLFWwindow* window,
                           _GLFWcursorWayland* cursorWayland)
{
    struct itimerspec timer = {0};
    struct wl_cursor* wlCursor = cursorWayland->cursor;
    struct wl_cursor_image* image;
    struct wl_buffer* buffer;
    struct wl_surface* surface = _glfw.wl.cursorSurface;
    int scale = 1;

    if (!wlCursor)
        buffer = cursorWayland->buffer;
    else
    {
        if (window->wl.contentScale > 1 && cursorWayland->cursorHiDPI)
        {
            wlCursor = cursorWayland->cursorHiDPI;
            scale = 2;
        }

        image = wlCursor->images[cursorWayland->currentImage];
        buffer = wl_cursor_image_get_buffer(image);
        if (!buffer)
            return;

        timer.it_value.tv_sec = image->delay / 1000;
        timer.it_value.tv_nsec = (image->delay % 1000) * 1000000;
        timerfd_settime(_glfw.wl.cursorTimerfd, 0, &timer, NULL);

        cursorWayland->width = image->width;
        cursorWayland->height = image->height;
        cursorWayland->xhot = image->hotspot_x;
        cursorWayland->yhot = image->hotspot_y;
    }

    wl_pointer_set_cursor(_glfw.wl.pointer, _glfw.wl.pointerEnterSerial,
                          surface,
                          cursorWayland->xhot / scale,
                          cursorWayland->yhot / scale);
    wl_surface_set_buffer_scale(surface, scale);
    wl_surface_attach(surface, buffer, 0, 0);
    wl_surface_damage(surface, 0, 0,
                      cursorWayland->width, cursorWayland->height);
    wl_surface_commit(surface);
}

static void incrementCursorImage(_GLFWwindow* window)
{
    _GLFWcursor* cursor;

    if (!window || window->wl.decorations.focus != GLFW_MAIN_WINDOW)
        return;

    cursor = window->wl.currentCursor;
    if (cursor && cursor->wl.cursor)
    {
        cursor->wl.currentImage += 1;
        cursor->wl.currentImage %= cursor->wl.cursor->image_count;
        setCursorImage(window, &cursor->wl);
    }
}

static GLFWbool flushDisplay(void)
{
    while (wl_display_flush(_glfw.wl.display) == -1)
    {
        if (errno != EAGAIN)
            return GLFW_FALSE;

        struct pollfd fd = { wl_display_get_fd(_glfw.wl.display), POLLOUT };

        while (poll(&fd, 1, -1) == -1)
        {
            if (errno != EINTR && errno != EAGAIN)
                return GLFW_FALSE;
        }
    }

    return GLFW_TRUE;
}

static int translateKey(uint32_t scancode)
{
    if (scancode < sizeof(_glfw.wl.keycodes) / sizeof(_glfw.wl.keycodes[0]))
        return _glfw.wl.keycodes[scancode];

    return GLFW_KEY_UNKNOWN;
}

static xkb_keysym_t composeSymbol(xkb_keysym_t sym)
{
    if (sym == XKB_KEY_NoSymbol || !_glfw.wl.xkb.composeState)
        return sym;
    if (xkb_compose_state_feed(_glfw.wl.xkb.composeState, sym)
            != XKB_COMPOSE_FEED_ACCEPTED)
        return sym;
    switch (xkb_compose_state_get_status(_glfw.wl.xkb.composeState))
    {
        case XKB_COMPOSE_COMPOSED:
            return xkb_compose_state_get_one_sym(_glfw.wl.xkb.composeState);
        case XKB_COMPOSE_COMPOSING:
        case XKB_COMPOSE_CANCELLED:
            return XKB_KEY_NoSymbol;
        case XKB_COMPOSE_NOTHING:
        default:
            return sym;
    }
}

static void inputText(_GLFWwindow* window, uint32_t scancode)
{
    const xkb_keysym_t* keysyms;
    const xkb_keycode_t keycode = scancode + 8;

    if (xkb_state_key_get_syms(_glfw.wl.xkb.state, keycode, &keysyms) == 1)
    {
        const xkb_keysym_t keysym = composeSymbol(keysyms[0]);
        const uint32_t codepoint = _glfwKeySym2Unicode(keysym);
        if (codepoint != GLFW_INVALID_CODEPOINT)
        {
            const int mods = _glfw.wl.xkb.modifiers;
            const int plain = !(mods & (GLFW_MOD_CONTROL | GLFW_MOD_ALT));
            _glfwInputChar(window, codepoint, mods, plain);
        }
    }
}

static void handleEvents(double* timeout)
{
#if defined(__linux__)
    _glfwDetectJoystickConnectionLinux();
#endif

    GLFWbool event = GLFW_FALSE;
    struct pollfd fds[4] =
    {
        { wl_display_get_fd(_glfw.wl.display), POLLIN },
        { _glfw.wl.keyRepeatTimerfd, POLLIN },
        { _glfw.wl.cursorTimerfd, POLLIN },
        { -1, POLLIN }
    };

    if (_glfw.wl.libdecor.context)
        fds[3].fd = libdecor_get_fd(_glfw.wl.libdecor.context);

    while (!event)
    {
        while (wl_display_prepare_read(_glfw.wl.display) != 0)
        {
            if (wl_display_dispatch_pending(_glfw.wl.display) > 0)
                return;
        }

        // If an error other than EAGAIN happens, we have likely been disconnected
        // from the Wayland session; try to handle that the best we can.
        if (!flushDisplay())
        {
            wl_display_cancel_read(_glfw.wl.display);

            _GLFWwindow* window = _glfw.windowListHead;
            while (window)
            {
                _glfwInputWindowCloseRequest(window);
                window = window->next;
            }

            return;
        }

        if (!waitForData(fds, sizeof(fds) / sizeof(fds[0]), timeout))
        {
            wl_display_cancel_read(_glfw.wl.display);
            return;
        }

        if (fds[0].revents & POLLIN)
        {
            wl_display_read_events(_glfw.wl.display);
            if (wl_display_dispatch_pending(_glfw.wl.display) > 0)
                event = GLFW_TRUE;
        }
        else
            wl_display_cancel_read(_glfw.wl.display);

        if (fds[1].revents & POLLIN)
        {
            uint64_t repeats;

            if (read(_glfw.wl.keyRepeatTimerfd, &repeats, sizeof(repeats)) == 8)
            {
                for (uint64_t i = 0; i < repeats; i++)
                {
                    _glfwInputKey(_glfw.wl.keyboardFocus,
                                  translateKey(_glfw.wl.keyRepeatScancode),
                                  _glfw.wl.keyRepeatScancode,
                                  GLFW_PRESS,
                                  _glfw.wl.xkb.modifiers);
                    inputText(_glfw.wl.keyboardFocus, _glfw.wl.keyRepeatScancode);
                }

                event = GLFW_TRUE;
            }
        }

        if (fds[2].revents & POLLIN)
        {
            uint64_t repeats;

            if (read(_glfw.wl.cursorTimerfd, &repeats, sizeof(repeats)) == 8)
                incrementCursorImage(_glfw.wl.pointerFocus);
        }

        if (fds[3].revents & POLLIN)
        {
            if (libdecor_dispatch(_glfw.wl.libdecor.context, 0) > 0)
                event = GLFW_TRUE;
        }
    }
}

// Reads the specified data offer as the specified MIME type
//
static char* readDataOfferAsString(struct wl_data_offer* offer, const char* mimeType)
{
    int fds[2];

    if (pipe2(fds, O_CLOEXEC) == -1)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to create pipe for data offer: %s",
                        strerror(errno));
        return NULL;
    }

    wl_data_offer_receive(offer, mimeType, fds[1]);
    flushDisplay();
    close(fds[1]);

    char* string = NULL;
    size_t size = 0;
    size_t length = 0;

    for (;;)
    {
        const size_t readSize = 4096;
        const size_t requiredSize = length + readSize + 1;
        if (requiredSize > size)
        {
            char* longer = realloc(string, requiredSize);
            if (!longer)
            {
                _glfwInputError(GLFW_OUT_OF_MEMORY, NULL);
                close(fds[0]);
                return NULL;
            }

            string = longer;
            size = requiredSize;
        }

        const ssize_t result = read(fds[0], string + length, readSize);
        if (result == 0)
            break;
        else if (result == -1)
        {
            if (errno == EINTR)
                continue;

            _glfwInputError(GLFW_PLATFORM_ERROR,
                            "Wayland: Failed to read from data offer pipe: %s",
                            strerror(errno));
            close(fds[0]);
            return NULL;
        }

        length += result;
    }

    close(fds[0]);

    string[length] = '\0';
    return string;
}

static void pointerHandleEnter(void* userData,
                               struct wl_pointer* pointer,
                               uint32_t serial,
                               struct wl_surface* surface,
                               wl_fixed_t sx,
                               wl_fixed_t sy)
{
    // Happens in the case we just destroyed the surface.
    if (!surface)
        return;

    if (wl_proxy_get_tag((struct wl_proxy*) surface) != &_glfw.wl.tag)
        return;

    _GLFWwindow* window = wl_surface_get_user_data(surface);

    if (surface == window->wl.decorations.top.surface)
        window->wl.decorations.focus = GLFW_TOP_DECORATION;
    else if (surface == window->wl.decorations.left.surface)
        window->wl.decorations.focus = GLFW_LEFT_DECORATION;
    else if (surface == window->wl.decorations.right.surface)
        window->wl.decorations.focus = GLFW_RIGHT_DECORATION;
    else if (surface == window->wl.decorations.bottom.surface)
        window->wl.decorations.focus = GLFW_BOTTOM_DECORATION;
    else
        window->wl.decorations.focus = GLFW_MAIN_WINDOW;

    _glfw.wl.serial = serial;
    _glfw.wl.pointerEnterSerial = serial;
    _glfw.wl.pointerFocus = window;

    window->wl.hovered = GLFW_TRUE;

    _glfwPlatformSetCursor(window, window->wl.currentCursor);
    _glfwInputCursorEnter(window, GLFW_TRUE);
}

static void pointerHandleLeave(void* userData,
                               struct wl_pointer* pointer,
                               uint32_t serial,
                               struct wl_surface* surface)
{
    if (!surface)
        return;

    if (wl_proxy_get_tag((struct wl_proxy*) surface) != &_glfw.wl.tag)
        return;

    _GLFWwindow* window = _glfw.wl.pointerFocus;
    if (!window)
        return;

    window->wl.hovered = GLFW_FALSE;

    _glfw.wl.serial = serial;
    _glfw.wl.pointerFocus = NULL;
    _glfw.wl.cursorPreviousName = NULL;
    _glfwInputCursorEnter(window, GLFW_FALSE);
}

static void pointerHandleMotion(void* userData,
                                struct wl_pointer* pointer,
                                uint32_t time,
                                wl_fixed_t sx,
                                wl_fixed_t sy)
{
    _GLFWwindow* window = _glfw.wl.pointerFocus;
    if (!window)
        return;

    if (window->cursorMode == GLFW_CURSOR_DISABLED)
        return;

    const double xpos = wl_fixed_to_double(sx);
    const double ypos = wl_fixed_to_double(sy);
    window->wl.cursorPosX = xpos;
    window->wl.cursorPosY = ypos;

    const char* cursorName = NULL;

    switch (window->wl.decorations.focus)
    {
        case GLFW_MAIN_WINDOW:
            _glfw.wl.cursorPreviousName = NULL;
            _glfwInputCursorPos(window, xpos, ypos);
            return;
        case GLFW_TOP_DECORATION:
            if (ypos < GLFW_BORDER_SIZE)
                cursorName = "n-resize";
            else
                cursorName = "left_ptr";
            break;
        case GLFW_LEFT_DECORATION:
            if (ypos < GLFW_BORDER_SIZE)
                cursorName = "nw-resize";
            else
                cursorName = "w-resize";
            break;
        case GLFW_RIGHT_DECORATION:
            if (ypos < GLFW_BORDER_SIZE)
                cursorName = "ne-resize";
            else
                cursorName = "e-resize";
            break;
        case GLFW_BOTTOM_DECORATION:
            if (xpos < GLFW_BORDER_SIZE)
                cursorName = "sw-resize";
            else if (xpos > window->wl.width + GLFW_BORDER_SIZE)
                cursorName = "se-resize";
            else
                cursorName = "s-resize";
            break;
        default:
            assert(0);
    }

    if (_glfw.wl.cursorPreviousName != cursorName)
    {
        struct wl_surface* surface = _glfw.wl.cursorSurface;
        struct wl_cursor_theme* theme = _glfw.wl.cursorTheme;
        int scale = 1;

        if (window->wl.contentScale > 1 && _glfw.wl.cursorThemeHiDPI)
        {
            // We only support up to scale=2 for now, since libwayland-cursor
            // requires us to load a different theme for each size.
            scale = 2;
            theme = _glfw.wl.cursorThemeHiDPI;
        }

        struct wl_cursor* cursor = wl_cursor_theme_get_cursor(theme, cursorName);
        if (!cursor)
            return;

        // TODO: handle animated cursors too.
        struct wl_cursor_image* image = cursor->images[0];
        if (!image)
            return;

        struct wl_buffer* buffer = wl_cursor_image_get_buffer(image);
        if (!buffer)
            return;

        wl_pointer_set_cursor(_glfw.wl.pointer, _glfw.wl.pointerEnterSerial,
                              surface,
                              image->hotspot_x / scale,
                              image->hotspot_y / scale);
        wl_surface_set_buffer_scale(surface, scale);
        wl_surface_attach(surface, buffer, 0, 0);
        wl_surface_damage(surface, 0, 0, image->width, image->height);
        wl_surface_commit(surface);

        _glfw.wl.cursorPreviousName = cursorName;
    }
}

static void pointerHandleButton(void* userData,
                                struct wl_pointer* pointer,
                                uint32_t serial,
                                uint32_t time,
                                uint32_t button,
                                uint32_t state)
{
    _GLFWwindow* window = _glfw.wl.pointerFocus;
    int glfwButton;

    uint32_t edges = XDG_TOPLEVEL_RESIZE_EDGE_NONE;

    if (!window)
        return;
    if (button == BTN_LEFT)
    {
        switch (window->wl.decorations.focus)
        {
            case GLFW_MAIN_WINDOW:
                break;
            case GLFW_TOP_DECORATION:
                if (window->wl.cursorPosY < GLFW_BORDER_SIZE)
                    edges = XDG_TOPLEVEL_RESIZE_EDGE_TOP;
                else
                {
                    xdg_toplevel_move(window->wl.xdg.toplevel, _glfw.wl.seat, serial);
                }
                break;
            case GLFW_LEFT_DECORATION:
                if (window->wl.cursorPosY < GLFW_BORDER_SIZE)
                    edges = XDG_TOPLEVEL_RESIZE_EDGE_TOP_LEFT;
                else
                    edges = XDG_TOPLEVEL_RESIZE_EDGE_LEFT;
                break;
            case GLFW_RIGHT_DECORATION:
                if (window->wl.cursorPosY < GLFW_BORDER_SIZE)
                    edges = XDG_TOPLEVEL_RESIZE_EDGE_TOP_RIGHT;
                else
                    edges = XDG_TOPLEVEL_RESIZE_EDGE_RIGHT;
                break;
            case GLFW_BOTTOM_DECORATION:
                if (window->wl.cursorPosX < GLFW_BORDER_SIZE)
                    edges = XDG_TOPLEVEL_RESIZE_EDGE_BOTTOM_LEFT;
                else if (window->wl.cursorPosX > window->wl.width + GLFW_BORDER_SIZE)
                    edges = XDG_TOPLEVEL_RESIZE_EDGE_BOTTOM_RIGHT;
                else
                    edges = XDG_TOPLEVEL_RESIZE_EDGE_BOTTOM;
                break;
            default:
                assert(0);
        }
        if (edges != XDG_TOPLEVEL_RESIZE_EDGE_NONE)
        {
            xdg_toplevel_resize(window->wl.xdg.toplevel, _glfw.wl.seat,
                                serial, edges);
            return;
        }
    }
    else if (button == BTN_RIGHT)
    {
        if (window->wl.decorations.focus != GLFW_MAIN_WINDOW &&
            window->wl.xdg.toplevel)
        {
            xdg_toplevel_show_window_menu(window->wl.xdg.toplevel,
                                          _glfw.wl.seat, serial,
                                          window->wl.cursorPosX,
                                          window->wl.cursorPosY);
            return;
        }
    }

    // Don’t pass the button to the user if it was related to a decoration.
    if (window->wl.decorations.focus != GLFW_MAIN_WINDOW)
        return;

    _glfw.wl.serial = serial;

    /* Makes left, right and middle 0, 1 and 2. Overall order follows evdev
     * codes. */
    glfwButton = button - BTN_LEFT;

    _glfwInputMouseClick(window,
                         glfwButton,
                         state == WL_POINTER_BUTTON_STATE_PRESSED
                                ? GLFW_PRESS
                                : GLFW_RELEASE,
                         _glfw.wl.xkb.modifiers);
}

static void pointerHandleAxis(void* userData,
                              struct wl_pointer* pointer,
                              uint32_t time,
                              uint32_t axis,
                              wl_fixed_t value)
{
    _GLFWwindow* window = _glfw.wl.pointerFocus;
    double x = 0.0, y = 0.0;
    // Wayland scroll events are in pointer motion coordinate space (think two
    // finger scroll).  The factor 10 is commonly used to convert to "scroll
    // step means 1.0.
    const double scrollFactor = 1.0 / 10.0;

    if (!window)
        return;

    assert(axis == WL_POINTER_AXIS_HORIZONTAL_SCROLL ||
           axis == WL_POINTER_AXIS_VERTICAL_SCROLL);

    if (axis == WL_POINTER_AXIS_HORIZONTAL_SCROLL)
        x = -wl_fixed_to_double(value) * scrollFactor;
    else if (axis == WL_POINTER_AXIS_VERTICAL_SCROLL)
        y = -wl_fixed_to_double(value) * scrollFactor;

    _glfwInputScroll(window, x, y);
}

static const struct wl_pointer_listener pointerListener =
{
    pointerHandleEnter,
    pointerHandleLeave,
    pointerHandleMotion,
    pointerHandleButton,
    pointerHandleAxis,
};

static void keyboardHandleKeymap(void* userData,
                                 struct wl_keyboard* keyboard,
                                 uint32_t format,
                                 int fd,
                                 uint32_t size)
{
    struct xkb_keymap* keymap;
    struct xkb_state* state;
    struct xkb_compose_table* composeTable;
    struct xkb_compose_state* composeState;
    char* mapStr;
    const char* locale;

    if (format != WL_KEYBOARD_KEYMAP_FORMAT_XKB_V1)
    {
        close(fd);
        return;
    }

    mapStr = mmap(NULL, size, PROT_READ, MAP_SHARED, fd, 0);
    if (mapStr == MAP_FAILED) {
        close(fd);
        return;
    }

    keymap = xkb_keymap_new_from_string(_glfw.wl.xkb.context,
                                        mapStr,
                                        XKB_KEYMAP_FORMAT_TEXT_V1,
                                        0);
    munmap(mapStr, size);
    close(fd);

    if (!keymap)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to compile keymap");
        return;
    }

    state = xkb_state_new(keymap);
    if (!state)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to create XKB state");
        xkb_keymap_unref(keymap);
        return;
    }

    // Look up the preferred locale, falling back to "C" as default.
    locale = getenv("LC_ALL");
    if (!locale)
        locale = getenv("LC_CTYPE");
    if (!locale)
        locale = getenv("LANG");
    if (!locale)
        locale = "C";

    composeTable =
        xkb_compose_table_new_from_locale(_glfw.wl.xkb.context, locale,
                                          XKB_COMPOSE_COMPILE_NO_FLAGS);
    if (composeTable)
    {
        composeState =
            xkb_compose_state_new(composeTable, XKB_COMPOSE_STATE_NO_FLAGS);
        xkb_compose_table_unref(composeTable);
        if (composeState)
            _glfw.wl.xkb.composeState = composeState;
        else
            _glfwInputError(GLFW_PLATFORM_ERROR,
                            "Wayland: Failed to create XKB compose state");
    }
    else
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to create XKB compose table");
    }

    xkb_keymap_unref(_glfw.wl.xkb.keymap);
    xkb_state_unref(_glfw.wl.xkb.state);
    _glfw.wl.xkb.keymap = keymap;
    _glfw.wl.xkb.state = state;

    _glfw.wl.xkb.controlIndex  = xkb_keymap_mod_get_index(_glfw.wl.xkb.keymap, "Control");
    _glfw.wl.xkb.altIndex      = xkb_keymap_mod_get_index(_glfw.wl.xkb.keymap, "Mod1");
    _glfw.wl.xkb.shiftIndex    = xkb_keymap_mod_get_index(_glfw.wl.xkb.keymap, "Shift");
    _glfw.wl.xkb.superIndex    = xkb_keymap_mod_get_index(_glfw.wl.xkb.keymap, "Mod4");
    _glfw.wl.xkb.capsLockIndex = xkb_keymap_mod_get_index(_glfw.wl.xkb.keymap, "Lock");
    _glfw.wl.xkb.numLockIndex  = xkb_keymap_mod_get_index(_glfw.wl.xkb.keymap, "Mod2");
}

static void keyboardHandleEnter(void* userData,
                                struct wl_keyboard* keyboard,
                                uint32_t serial,
                                struct wl_surface* surface,
                                struct wl_array* keys)
{
    // Happens in the case we just destroyed the surface.
    if (!surface)
        return;

    if (wl_proxy_get_tag((struct wl_proxy*) surface) != &_glfw.wl.tag)
        return;

    _GLFWwindow* window = wl_surface_get_user_data(surface);
    if (surface != window->wl.surface)
        return;

    _glfw.wl.serial = serial;
    _glfw.wl.keyboardFocus = window;
    _glfwInputWindowFocus(window, GLFW_TRUE);
}

static void keyboardHandleLeave(void* userData,
                                struct wl_keyboard* keyboard,
                                uint32_t serial,
                                struct wl_surface* surface)
{
    _GLFWwindow* window = _glfw.wl.keyboardFocus;

    if (!window)
        return;

    struct itimerspec timer = {0};
    timerfd_settime(_glfw.wl.keyRepeatTimerfd, 0, &timer, NULL);

    _glfw.wl.serial = serial;
    _glfw.wl.keyboardFocus = NULL;
    _glfwInputWindowFocus(window, GLFW_FALSE);
}

static void keyboardHandleKey(void* userData,
                              struct wl_keyboard* keyboard,
                              uint32_t serial,
                              uint32_t time,
                              uint32_t scancode,
                              uint32_t state)
{
    _GLFWwindow* window = _glfw.wl.keyboardFocus;
    if (!window)
        return;

    const int key = translateKey(scancode);
    const int action =
        state == WL_KEYBOARD_KEY_STATE_PRESSED ? GLFW_PRESS : GLFW_RELEASE;

    _glfw.wl.serial = serial;

    struct itimerspec timer = {0};

    if (action == GLFW_PRESS)
    {
        const xkb_keycode_t keycode = scancode + 8;

        if (xkb_keymap_key_repeats(_glfw.wl.xkb.keymap, keycode) &&
            _glfw.wl.keyRepeatRate > 0)
        {
            _glfw.wl.keyRepeatScancode = scancode;
            if (_glfw.wl.keyRepeatRate > 1)
                timer.it_interval.tv_nsec = 1000000000 / _glfw.wl.keyRepeatRate;
            else
                timer.it_interval.tv_sec = 1;

            timer.it_value.tv_sec = _glfw.wl.keyRepeatDelay / 1000;
            timer.it_value.tv_nsec = (_glfw.wl.keyRepeatDelay % 1000) * 1000000;
        }
    }

    timerfd_settime(_glfw.wl.keyRepeatTimerfd, 0, &timer, NULL);

    _glfwInputKey(window, key, scancode, action, _glfw.wl.xkb.modifiers);

    if (action == GLFW_PRESS)
        inputText(window, scancode);
}

static void keyboardHandleModifiers(void* userData,
                                    struct wl_keyboard* keyboard,
                                    uint32_t serial,
                                    uint32_t modsDepressed,
                                    uint32_t modsLatched,
                                    uint32_t modsLocked,
                                    uint32_t group)
{
    _glfw.wl.serial = serial;

    if (!_glfw.wl.xkb.keymap)
        return;

    xkb_state_update_mask(_glfw.wl.xkb.state,
                          modsDepressed,
                          modsLatched,
                          modsLocked,
                          0,
                          0,
                          group);

    _glfw.wl.xkb.modifiers = 0;

    struct
    {
        xkb_mod_index_t index;
        unsigned int bit;
    } modifiers[] =
    {
        { _glfw.wl.xkb.controlIndex,  GLFW_MOD_CONTROL },
        { _glfw.wl.xkb.altIndex,      GLFW_MOD_ALT },
        { _glfw.wl.xkb.shiftIndex,    GLFW_MOD_SHIFT },
        { _glfw.wl.xkb.superIndex,    GLFW_MOD_SUPER },
        { _glfw.wl.xkb.capsLockIndex, GLFW_MOD_CAPS_LOCK },
        { _glfw.wl.xkb.numLockIndex,  GLFW_MOD_NUM_LOCK }
    };

    for (size_t i = 0; i < sizeof(modifiers) / sizeof(modifiers[0]); i++)
    {
        if (xkb_state_mod_index_is_active(_glfw.wl.xkb.state,
                                          modifiers[i].index,
                                          XKB_STATE_MODS_EFFECTIVE) == 1)
        {
            _glfw.wl.xkb.modifiers |= modifiers[i].bit;
        }
    }
}

#ifdef WL_KEYBOARD_REPEAT_INFO_SINCE_VERSION
static void keyboardHandleRepeatInfo(void* userData,
                                     struct wl_keyboard* keyboard,
                                     int32_t rate,
                                     int32_t delay)
{
    if (keyboard != _glfw.wl.keyboard)
        return;

    _glfw.wl.keyRepeatRate = rate;
    _glfw.wl.keyRepeatDelay = delay;
}
#endif

static const struct wl_keyboard_listener keyboardListener =
{
    keyboardHandleKeymap,
    keyboardHandleEnter,
    keyboardHandleLeave,
    keyboardHandleKey,
    keyboardHandleModifiers,
#ifdef WL_KEYBOARD_REPEAT_INFO_SINCE_VERSION
    keyboardHandleRepeatInfo,
#endif
};

static void seatHandleCapabilities(void* userData,
                                   struct wl_seat* seat,
                                   enum wl_seat_capability caps)
{
    if ((caps & WL_SEAT_CAPABILITY_POINTER) && !_glfw.wl.pointer)
    {
        _glfw.wl.pointer = wl_seat_get_pointer(seat);
        wl_pointer_add_listener(_glfw.wl.pointer, &pointerListener, NULL);
    }
    else if (!(caps & WL_SEAT_CAPABILITY_POINTER) && _glfw.wl.pointer)
    {
        wl_pointer_destroy(_glfw.wl.pointer);
        _glfw.wl.pointer = NULL;
    }

    if ((caps & WL_SEAT_CAPABILITY_KEYBOARD) && !_glfw.wl.keyboard)
    {
        _glfw.wl.keyboard = wl_seat_get_keyboard(seat);
        wl_keyboard_add_listener(_glfw.wl.keyboard, &keyboardListener, NULL);
    }
    else if (!(caps & WL_SEAT_CAPABILITY_KEYBOARD) && _glfw.wl.keyboard)
    {
        wl_keyboard_destroy(_glfw.wl.keyboard);
        _glfw.wl.keyboard = NULL;
    }
}

static void seatHandleName(void* userData,
                           struct wl_seat* seat,
                           const char* name)
{
}

static const struct wl_seat_listener seatListener =
{
    seatHandleCapabilities,
    seatHandleName,
};

static void dataOfferHandleOffer(void* userData,
                                 struct wl_data_offer* offer,
                                 const char* mimeType)
{
    for (unsigned int i = 0; i < _glfw.wl.offerCount; i++)
    {
        if (_glfw.wl.offers[i].offer == offer)
        {
            if (strcmp(mimeType, "text/plain;charset=utf-8") == 0)
                _glfw.wl.offers[i].text_plain_utf8 = GLFW_TRUE;
            else if (strcmp(mimeType, "text/uri-list") == 0)
                _glfw.wl.offers[i].text_uri_list = GLFW_TRUE;

            break;
        }
    }
}

static const struct wl_data_offer_listener dataOfferListener =
{
    dataOfferHandleOffer
};

static void dataDeviceHandleDataOffer(void* userData,
                                      struct wl_data_device* device,
                                      struct wl_data_offer* offer)
{
    _GLFWofferWayland* offers =
        realloc(_glfw.wl.offers,
                sizeof(_GLFWofferWayland) * (_glfw.wl.offerCount + 1));
    if (!offers)
    {
        _glfwInputError(GLFW_OUT_OF_MEMORY, NULL);
        return;
    }

    _glfw.wl.offers = offers;
    _glfw.wl.offerCount++;

    _glfw.wl.offers[_glfw.wl.offerCount - 1] = (_GLFWofferWayland) { offer };
    wl_data_offer_add_listener(offer, &dataOfferListener, NULL);
}

static void dataDeviceHandleEnter(void* userData,
                                  struct wl_data_device* device,
                                  uint32_t serial,
                                  struct wl_surface* surface,
                                  wl_fixed_t x,
                                  wl_fixed_t y,
                                  struct wl_data_offer* offer)
{
    if (_glfw.wl.dragOffer)
    {
        wl_data_offer_destroy(_glfw.wl.dragOffer);
        _glfw.wl.dragOffer = NULL;
        _glfw.wl.dragFocus = NULL;
    }

    for (unsigned int i = 0; i < _glfw.wl.offerCount; i++)
    {
        if (_glfw.wl.offers[i].offer == offer)
        {
            _GLFWwindow* window = NULL;

            if (surface)
            {
                if (wl_proxy_get_tag((struct wl_proxy*) surface) == &_glfw.wl.tag)
                    window = wl_surface_get_user_data(surface);
            }

            if (surface == window->wl.surface && _glfw.wl.offers[i].text_uri_list)
            {
                _glfw.wl.dragOffer = offer;
                _glfw.wl.dragFocus = window;
                _glfw.wl.dragSerial = serial;
            }

            _glfw.wl.offers[i] = _glfw.wl.offers[_glfw.wl.offerCount - 1];
            _glfw.wl.offerCount--;
            break;
        }
    }

    if (wl_proxy_get_tag((struct wl_proxy*) surface) != &_glfw.wl.tag)
        return;

    if (_glfw.wl.dragOffer)
        wl_data_offer_accept(offer, serial, "text/uri-list");
    else
    {
        wl_data_offer_accept(offer, serial, NULL);
        wl_data_offer_destroy(offer);
    }
}

static void dataDeviceHandleLeave(void* userData,
                                  struct wl_data_device* device)
{
    if (_glfw.wl.dragOffer)
    {
        wl_data_offer_destroy(_glfw.wl.dragOffer);
        _glfw.wl.dragOffer = NULL;
        _glfw.wl.dragFocus = NULL;
    }
}

static void dataDeviceHandleMotion(void* userData,
                                   struct wl_data_device* device,
                                   uint32_t time,
                                   wl_fixed_t x,
                                   wl_fixed_t y)
{
}

static void dataDeviceHandleDrop(void* userData,
                                 struct wl_data_device* device)
{
    if (!_glfw.wl.dragOffer)
        return;

    char* string = readDataOfferAsString(_glfw.wl.dragOffer, "text/uri-list");
    if (string)
    {
        int count;
        char** paths = _glfwParseUriList(string, &count);
        if (paths)
            _glfwInputDrop(_glfw.wl.dragFocus, count, (const char**) paths);

        for (int i = 0; i < count; i++)
            free(paths[i]);

        free(paths);
    }

    free(string);
}

static void dataDeviceHandleSelection(void* userData,
                                      struct wl_data_device* device,
                                      struct wl_data_offer* offer)
{
    if (_glfw.wl.selectionOffer)
    {
        wl_data_offer_destroy(_glfw.wl.selectionOffer);
        _glfw.wl.selectionOffer = NULL;
    }

    for (unsigned int i = 0; i < _glfw.wl.offerCount; i++)
    {
        if (_glfw.wl.offers[i].offer == offer)
        {
            if (_glfw.wl.offers[i].text_plain_utf8)
                _glfw.wl.selectionOffer = offer;
            else
                wl_data_offer_destroy(offer);

            _glfw.wl.offers[i] = _glfw.wl.offers[_glfw.wl.offerCount - 1];
            _glfw.wl.offerCount--;
            break;
        }
    }
}

const struct wl_data_device_listener dataDeviceListener =
{
    dataDeviceHandleDataOffer,
    dataDeviceHandleEnter,
    dataDeviceHandleLeave,
    dataDeviceHandleMotion,
    dataDeviceHandleDrop,
    dataDeviceHandleSelection,
};

// Translates a GLFW standard cursor to a theme cursor name
//
static char *translateCursorShape(int shape)
{
    switch (shape)
    {
        case GLFW_ARROW_CURSOR:
            return "left_ptr";
        case GLFW_IBEAM_CURSOR:
            return "xterm";
        case GLFW_CROSSHAIR_CURSOR:
            return "crosshair";
        case GLFW_HAND_CURSOR:
            return "hand2";
        case GLFW_HRESIZE_CURSOR:
            return "sb_h_double_arrow";
        case GLFW_VRESIZE_CURSOR:
            return "sb_v_double_arrow";
    }
    return NULL;
}

void _glfwAddSeatListenerWayland(struct wl_seat* seat)
{
    wl_seat_add_listener(seat, &seatListener, NULL);
}

void _glfwAddDataDeviceListenerWayland(struct wl_data_device* device)
{
    wl_data_device_add_listener(device, &dataDeviceListener, NULL);
}


//////////////////////////////////////////////////////////////////////////
//////                       GLFW platform API                      //////
//////////////////////////////////////////////////////////////////////////

int _glfwPlatformCreateWindow(_GLFWwindow* window,
                              const _GLFWwndconfig* wndconfig,
                              const _GLFWctxconfig* ctxconfig,
                              const _GLFWfbconfig* fbconfig)
{
    if (!createNativeSurface(window, wndconfig, fbconfig))
        return GLFW_FALSE;

    if (ctxconfig->client != GLFW_NO_API)
    {
        if (ctxconfig->source == GLFW_EGL_CONTEXT_API ||
            ctxconfig->source == GLFW_NATIVE_CONTEXT_API)
        {
            window->wl.egl.window = wl_egl_window_create(window->wl.surface,
                                                         wndconfig->width,
                                                         wndconfig->height);
            if (!window->wl.egl.window)
            {
                _glfwInputError(GLFW_PLATFORM_ERROR,
                                "Wayland: Failed to create EGL window");
                return GLFW_FALSE;
            }

            if (!_glfwInitEGL())
                return GLFW_FALSE;
            if (!_glfwCreateContextEGL(window, ctxconfig, fbconfig))
                return GLFW_FALSE;
        }
        else if (ctxconfig->source == GLFW_OSMESA_CONTEXT_API)
        {
            if (!_glfwInitOSMesa())
                return GLFW_FALSE;
            if (!_glfwCreateContextOSMesa(window, ctxconfig, fbconfig))
                return GLFW_FALSE;
        }

        if (!_glfwRefreshContextAttribs(window, ctxconfig))
            return GLFW_FALSE;
    }

    if (window->monitor || wndconfig->visible)
    {
        if (!createShellObjects(window))
            return GLFW_FALSE;
    }

    return GLFW_TRUE;
}

void _glfwPlatformDestroyWindow(_GLFWwindow* window)
{
    if (window == _glfw.wl.pointerFocus)
        _glfw.wl.pointerFocus = NULL;

    if (window == _glfw.wl.keyboardFocus)
        _glfw.wl.keyboardFocus = NULL;

    if (window->wl.idleInhibitor)
        zwp_idle_inhibitor_v1_destroy(window->wl.idleInhibitor);

    if (window->wl.relativePointer)
        zwp_relative_pointer_v1_destroy(window->wl.relativePointer);

    if (window->wl.lockedPointer)
        zwp_locked_pointer_v1_destroy(window->wl.lockedPointer);

    if (window->context.destroy)
        window->context.destroy(window);

    destroyShellObjects(window);

    if (window->wl.decorations.buffer)
        wl_buffer_destroy(window->wl.decorations.buffer);

    if (window->wl.egl.window)
        wl_egl_window_destroy(window->wl.egl.window);

    if (window->wl.surface)
        wl_surface_destroy(window->wl.surface);

    free(window->wl.title);
    free(window->wl.scales);
}

void _glfwPlatformSetWindowTitle(_GLFWwindow* window, const char* title)
{
    if (window->wl.title)
        free(window->wl.title);
    window->wl.title = _glfw_strdup(title);

    if (window->wl.libdecor.frame)
        libdecor_frame_set_title(window->wl.libdecor.frame, title);
    else if (window->wl.xdg.toplevel)
        xdg_toplevel_set_title(window->wl.xdg.toplevel, title);
}

void _glfwPlatformSetWindowIcon(_GLFWwindow* window,
                                int count, const GLFWimage* images)
{
    _glfwInputError(GLFW_PLATFORM_ERROR,
                    "Wayland: Setting window icon not supported");
}

void _glfwPlatformGetWindowPos(_GLFWwindow* window, int* xpos, int* ypos)
{
    // A Wayland client is not aware of its position, so just warn and leave it
    // as (0, 0)

    _glfwInputError(GLFW_PLATFORM_ERROR,
                    "Wayland: Window position retrieval not supported");
}

void _glfwPlatformSetWindowPos(_GLFWwindow* window, int xpos, int ypos)
{
    // A Wayland client can not set its position, so just warn

    _glfwInputError(GLFW_PLATFORM_ERROR,
                    "Wayland: Window position setting not supported");
}

void _glfwPlatformGetWindowSize(_GLFWwindow* window, int* width, int* height)
{
    if (width)
        *width = window->wl.width;
    if (height)
        *height = window->wl.height;
}

void _glfwPlatformSetWindowSize(_GLFWwindow* window, int width, int height)
{
    if (window->monitor)
    {
        // Video mode setting is not available on Wayland
    }
    else
    {
        window->wl.width = width;
        window->wl.height = height;
        resizeWindow(window);

        if (window->wl.libdecor.frame)
        {
            struct libdecor_state* frameState = libdecor_state_new(width, height);
            libdecor_frame_commit(window->wl.libdecor.frame, frameState, NULL);
            libdecor_state_free(frameState);
        }

        if (window->wl.visible)
            _glfwInputWindowDamage(window);
    }
}

void _glfwPlatformSetWindowSizeLimits(_GLFWwindow* window,
                                      int minwidth, int minheight,
                                      int maxwidth, int maxheight)
{
    if (window->wl.libdecor.frame)
    {
        if (minwidth == GLFW_DONT_CARE || minheight == GLFW_DONT_CARE)
            minwidth = minheight = 0;

        if (maxwidth == GLFW_DONT_CARE || maxheight == GLFW_DONT_CARE)
            maxwidth = maxheight = 0;

        libdecor_frame_set_min_content_size(window->wl.libdecor.frame,
                                            minwidth, minheight);
        libdecor_frame_set_max_content_size(window->wl.libdecor.frame,
                                            maxwidth, maxheight);
    }
    else if (window->wl.xdg.toplevel)
    {
        if (minwidth == GLFW_DONT_CARE || minheight == GLFW_DONT_CARE)
            minwidth = minheight = 0;
        else
        {
            if (window->wl.decorations.top.surface)
            {
                minwidth  += GLFW_BORDER_SIZE * 2;
                minheight += GLFW_CAPTION_HEIGHT + GLFW_BORDER_SIZE;
            }
        }

        if (maxwidth == GLFW_DONT_CARE || maxheight == GLFW_DONT_CARE)
            maxwidth = maxheight = 0;
        else
        {
            if (window->wl.decorations.top.surface)
            {
                maxwidth  += GLFW_BORDER_SIZE * 2;
                maxheight += GLFW_CAPTION_HEIGHT + GLFW_BORDER_SIZE;
            }
        }

        xdg_toplevel_set_min_size(window->wl.xdg.toplevel, minwidth, minheight);
        xdg_toplevel_set_max_size(window->wl.xdg.toplevel, maxwidth, maxheight);
        wl_surface_commit(window->wl.surface);
    }
}

void _glfwPlatformSetWindowAspectRatio(_GLFWwindow* window,
                                       int numer, int denom)
{
    if (window->wl.maximized || window->wl.fullscreen)
        return;

    int width = window->wl.width, height = window->wl.height;

    if (numer != GLFW_DONT_CARE && denom != GLFW_DONT_CARE)
    {
        const float aspectRatio = (float) width / (float) height;
        const float targetRatio = (float) numer / (float) denom;
        if (aspectRatio < targetRatio)
            height /= targetRatio;
        else if (aspectRatio > targetRatio)
            width *= targetRatio;
    }

    if (width != window->wl.width || height != window->wl.height)
    {
        window->wl.width = width;
        window->wl.height = height;
        resizeWindow(window);

        if (window->wl.libdecor.frame)
        {
            struct libdecor_state* frameState = libdecor_state_new(width, height);
            libdecor_frame_commit(window->wl.libdecor.frame, frameState, NULL);
            libdecor_state_free(frameState);
        }

        _glfwInputWindowSize(window, width, height);

        if (window->wl.visible)
            _glfwInputWindowDamage(window);
    }
}

void _glfwPlatformGetFramebufferSize(_GLFWwindow* window,
                                     int* width, int* height)
{
    _glfwPlatformGetWindowSize(window, width, height);
    if (width)
        *width *= window->wl.contentScale;
    if (height)
        *height *= window->wl.contentScale;
}

void _glfwPlatformGetWindowFrameSize(_GLFWwindow* window,
                                     int* left, int* top,
                                     int* right, int* bottom)
{
    if (window->wl.decorations.top.surface)
    {
        if (top)
            *top = GLFW_CAPTION_HEIGHT;
        if (left)
            *left = GLFW_BORDER_SIZE;
        if (right)
            *right = GLFW_BORDER_SIZE;
        if (bottom)
            *bottom = GLFW_BORDER_SIZE;
    }
}

void _glfwPlatformGetWindowContentScale(_GLFWwindow* window,
                                        float* xscale, float* yscale)
{
    if (xscale)
        *xscale = (float) window->wl.contentScale;
    if (yscale)
        *yscale = (float) window->wl.contentScale;
}

void _glfwPlatformIconifyWindow(_GLFWwindow* window)
{
    if (window->wl.libdecor.frame)
        libdecor_frame_set_minimized(window->wl.libdecor.frame);
    else if (window->wl.xdg.toplevel)
        xdg_toplevel_set_minimized(window->wl.xdg.toplevel);
}

void _glfwPlatformRestoreWindow(_GLFWwindow* window)
{
    if (window->monitor)
    {
        // There is no way to unset minimized, or even to know if we are
        // minimized, so there is nothing to do here.
    }
    else
    {
        // We assume we are not minimized and act only on maximization

        if (window->wl.maximized)
        {
            if (window->wl.libdecor.frame)
                libdecor_frame_unset_maximized(window->wl.libdecor.frame);
            else if (window->wl.xdg.toplevel)
                xdg_toplevel_unset_maximized(window->wl.xdg.toplevel);
            else
                window->wl.maximized = GLFW_FALSE;
        }
    }
}

void _glfwPlatformMaximizeWindow(_GLFWwindow* window)
{
    if (window->wl.libdecor.frame)
        libdecor_frame_set_maximized(window->wl.libdecor.frame);
    else if (window->wl.xdg.toplevel)
        xdg_toplevel_set_maximized(window->wl.xdg.toplevel);
    else
        window->wl.maximized = GLFW_TRUE;
}

void _glfwPlatformShowWindow(_GLFWwindow* window)
{
    if (!window->wl.libdecor.frame && !window->wl.xdg.toplevel)
    {
        // NOTE: The XDG/shell surface is created here so command-line applications
        //       with off-screen windows do not appear in for example the Unity dock
        createShellObjects(window);
    }
}

void _glfwPlatformHideWindow(_GLFWwindow* window)
{
    if (window->wl.visible)
    {
        window->wl.visible = GLFW_FALSE;
        destroyShellObjects(window);

        wl_surface_attach(window->wl.surface, NULL, 0, 0);
        wl_surface_commit(window->wl.surface);
    }
}

void _glfwPlatformRequestWindowAttention(_GLFWwindow* window)
{
    // TODO
    _glfwInputError(GLFW_PLATFORM_ERROR,
                    "Wayland: Window attention request not implemented yet");
}

void _glfwPlatformFocusWindow(_GLFWwindow* window)
{
    _glfwInputError(GLFW_PLATFORM_ERROR,
                    "Wayland: Focusing a window requires user interaction");
}

void _glfwPlatformSetWindowMonitor(_GLFWwindow* window,
                                   _GLFWmonitor* monitor,
                                   int xpos, int ypos,
                                   int width, int height,
                                   int refreshRate)
{
    if (window->monitor == monitor)
    {
        if (!monitor)
            _glfwPlatformSetWindowSize(window, width, height);

        return;
    }

    if (window->monitor)
        releaseMonitor(window);

    _glfwInputWindowMonitor(window, monitor);

    if (window->monitor)
        acquireMonitor(window);
    else
        _glfwPlatformSetWindowSize(window, width, height);
}

int _glfwPlatformWindowFocused(_GLFWwindow* window)
{
    return _glfw.wl.keyboardFocus == window;
}

int _glfwPlatformWindowIconified(_GLFWwindow* window)
{
    // xdg-shell doesn’t give any way to request whether a surface is iconified
    return GLFW_FALSE;
}

int _glfwPlatformWindowVisible(_GLFWwindow* window)
{
    return window->wl.visible;
}

int _glfwPlatformWindowMaximized(_GLFWwindow* window)
{
    return window->wl.maximized;
}

int _glfwPlatformWindowHovered(_GLFWwindow* window)
{
    return window->wl.hovered;
}

int _glfwPlatformFramebufferTransparent(_GLFWwindow* window)
{
    return window->wl.transparent;
}

void _glfwPlatformSetWindowResizable(_GLFWwindow* window, GLFWbool enabled)
{
    if (window->wl.libdecor.frame)
    {
        if (enabled)
        {
            libdecor_frame_set_capabilities(window->wl.libdecor.frame,
                                            LIBDECOR_ACTION_RESIZE);
        }
        else
        {
            libdecor_frame_unset_capabilities(window->wl.libdecor.frame,
                                              LIBDECOR_ACTION_RESIZE);
        }
    }
    else
    {
        // TODO
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Window attribute setting not implemented yet");
    }
}

void _glfwPlatformSetWindowDecorated(_GLFWwindow* window, GLFWbool enabled)
{
    if (window->wl.libdecor.frame)
    {
        libdecor_frame_set_visibility(window->wl.libdecor.frame, enabled);
    }
    else if (window->wl.xdg.decoration)
    {
        uint32_t mode;

        if (enabled)
            mode = ZXDG_TOPLEVEL_DECORATION_V1_MODE_SERVER_SIDE;
        else
            mode = ZXDG_TOPLEVEL_DECORATION_V1_MODE_CLIENT_SIDE;

        zxdg_toplevel_decoration_v1_set_mode(window->wl.xdg.decoration, mode);
    }
    else if (window->wl.xdg.toplevel)
    {
        if (enabled)
            createFallbackDecorations(window);
        else
            destroyFallbackDecorations(window);
    }
}

void _glfwPlatformSetWindowFloating(_GLFWwindow* window, GLFWbool enabled)
{
    // TODO
    _glfwInputError(GLFW_PLATFORM_ERROR,
                    "Wayland: Window attribute setting not implemented yet");
}

float _glfwPlatformGetWindowOpacity(_GLFWwindow* window)
{
    return 1.f;
}

void _glfwPlatformSetWindowOpacity(_GLFWwindow* window, float opacity)
{
}

void _glfwPlatformSetRawMouseMotion(_GLFWwindow* window, GLFWbool enabled)
{
    // This is handled in relativePointerHandleRelativeMotion
}

GLFWbool _glfwPlatformRawMouseMotionSupported(void)
{
    return GLFW_TRUE;
}

void _glfwPlatformPollEvents(void)
{
    double timeout = 0.0;
    handleEvents(&timeout);
}

void _glfwPlatformWaitEvents(void)
{
    handleEvents(NULL);
}

void _glfwPlatformWaitEventsTimeout(double timeout)
{
    handleEvents(&timeout);
}

void _glfwPlatformPostEmptyEvent(void)
{
    wl_display_sync(_glfw.wl.display);
    flushDisplay();
}

void _glfwPlatformGetCursorPos(_GLFWwindow* window, double* xpos, double* ypos)
{
    if (xpos)
        *xpos = window->wl.cursorPosX;
    if (ypos)
        *ypos = window->wl.cursorPosY;
}

void _glfwPlatformSetCursorPos(_GLFWwindow* window, double x, double y)
{
}

void _glfwPlatformSetCursorMode(_GLFWwindow* window, int mode)
{
    _glfwPlatformSetCursor(window, window->wl.currentCursor);
}

const char* _glfwPlatformGetScancodeName(int scancode)
{
    if (scancode < 0 || scancode > 255 ||
        _glfw.wl.keycodes[scancode] == GLFW_KEY_UNKNOWN)
    {
        _glfwInputError(GLFW_INVALID_VALUE,
                        "Wayland: Invalid scancode %i",
                        scancode);
        return NULL;
    }

    const int key = _glfw.wl.keycodes[scancode];
    const xkb_keycode_t keycode = scancode + 8;
    const xkb_layout_index_t layout =
        xkb_state_key_get_layout(_glfw.wl.xkb.state, keycode);
    if (layout == XKB_LAYOUT_INVALID)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to retrieve layout for key name");
        return NULL;
    }

    const xkb_keysym_t* keysyms = NULL;
    xkb_keymap_key_get_syms_by_level(_glfw.wl.xkb.keymap,
                                     keycode,
                                     layout,
                                     0,
                                     &keysyms);
    if (keysyms == NULL)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to retrieve keysym for key name");
        return NULL;
    }

    const uint32_t codepoint = _glfwKeySym2Unicode(keysyms[0]);
    if (codepoint == GLFW_INVALID_CODEPOINT)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to retrieve codepoint for key name");
        return NULL;
    }

    const size_t count = _glfwEncodeUTF8(_glfw.wl.keynames[key],  codepoint);
    if (count == 0)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to encode codepoint for key name");
        return NULL;
    }

    _glfw.wl.keynames[key][count] = '\0';
    return _glfw.wl.keynames[key];
}

int _glfwPlatformGetKeyScancode(int key)
{
    return _glfw.wl.scancodes[key];
}

int _glfwPlatformCreateCursor(_GLFWcursor* cursor,
                              const GLFWimage* image,
                              int xhot, int yhot)
{
    cursor->wl.buffer = createShmBuffer(image);
    if (!cursor->wl.buffer)
        return GLFW_FALSE;

    cursor->wl.width = image->width;
    cursor->wl.height = image->height;
    cursor->wl.xhot = xhot;
    cursor->wl.yhot = yhot;
    return GLFW_TRUE;
}

int _glfwPlatformCreateStandardCursor(_GLFWcursor* cursor, int shape)
{
    struct wl_cursor* standardCursor;

    standardCursor = wl_cursor_theme_get_cursor(_glfw.wl.cursorTheme,
                                                translateCursorShape(shape));
    if (!standardCursor)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Standard cursor \"%s\" not found",
                        translateCursorShape(shape));
        return GLFW_FALSE;
    }

    cursor->wl.cursor = standardCursor;
    cursor->wl.currentImage = 0;

    if (_glfw.wl.cursorThemeHiDPI)
    {
        standardCursor = wl_cursor_theme_get_cursor(_glfw.wl.cursorThemeHiDPI,
                                                    translateCursorShape(shape));
        cursor->wl.cursorHiDPI = standardCursor;
    }

    return GLFW_TRUE;
}

void _glfwPlatformDestroyCursor(_GLFWcursor* cursor)
{
    // If it's a standard cursor we don't need to do anything here
    if (cursor->wl.cursor)
        return;

    if (cursor->wl.buffer)
        wl_buffer_destroy(cursor->wl.buffer);
}

static void relativePointerHandleRelativeMotion(void* userData,
                                                struct zwp_relative_pointer_v1* pointer,
                                                uint32_t timeHi,
                                                uint32_t timeLo,
                                                wl_fixed_t dx,
                                                wl_fixed_t dy,
                                                wl_fixed_t dxUnaccel,
                                                wl_fixed_t dyUnaccel)
{
    _GLFWwindow* window = userData;
    double xpos = window->virtualCursorPosX;
    double ypos = window->virtualCursorPosY;

    if (window->cursorMode != GLFW_CURSOR_DISABLED)
        return;

    if (window->rawMouseMotion)
    {
        xpos += wl_fixed_to_double(dxUnaccel);
        ypos += wl_fixed_to_double(dyUnaccel);
    }
    else
    {
        xpos += wl_fixed_to_double(dx);
        ypos += wl_fixed_to_double(dy);
    }

    _glfwInputCursorPos(window, xpos, ypos);
}

static const struct zwp_relative_pointer_v1_listener relativePointerListener =
{
    relativePointerHandleRelativeMotion
};

static void lockedPointerHandleLocked(void* userData,
                                      struct zwp_locked_pointer_v1* lockedPointer)
{
}

static void lockedPointerHandleUnlocked(void* userData,
                                        struct zwp_locked_pointer_v1* lockedPointer)
{
}

static const struct zwp_locked_pointer_v1_listener lockedPointerListener =
{
    lockedPointerHandleLocked,
    lockedPointerHandleUnlocked
};

static void lockPointer(_GLFWwindow* window)
{
    if (!_glfw.wl.relativePointerManager)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: no relative pointer manager");
        return;
    }

    window->wl.relativePointer =
        zwp_relative_pointer_manager_v1_get_relative_pointer(
            _glfw.wl.relativePointerManager,
            _glfw.wl.pointer);
    zwp_relative_pointer_v1_add_listener(window->wl.relativePointer,
                                         &relativePointerListener,
                                         window);

    window->wl.lockedPointer =
        zwp_pointer_constraints_v1_lock_pointer(
            _glfw.wl.pointerConstraints,
            window->wl.surface,
            _glfw.wl.pointer,
            NULL,
            ZWP_POINTER_CONSTRAINTS_V1_LIFETIME_PERSISTENT);
    zwp_locked_pointer_v1_add_listener(window->wl.lockedPointer,
                                       &lockedPointerListener,
                                       window);
}

static void unlockPointer(_GLFWwindow* window)
{
    zwp_relative_pointer_v1_destroy(window->wl.relativePointer);
    window->wl.relativePointer = NULL;

    zwp_locked_pointer_v1_destroy(window->wl.lockedPointer);
    window->wl.lockedPointer = NULL;
}

void _glfwPlatformSetCursor(_GLFWwindow* window, _GLFWcursor* cursor)
{
    if (!_glfw.wl.pointer)
        return;

    window->wl.currentCursor = cursor;

    // If we're not in the correct window just save the cursor
    // the next time the pointer enters the window the cursor will change
    if (window != _glfw.wl.pointerFocus ||
        window->wl.decorations.focus != GLFW_MAIN_WINDOW)
    {
        return;
    }

    // Update pointer lock to match cursor mode
    if (window->cursorMode == GLFW_CURSOR_DISABLED)
    {
        if (!window->wl.lockedPointer)
            lockPointer(window);
    }
    else if (window->cursorMode == GLFW_CURSOR_NORMAL ||
             window->cursorMode == GLFW_CURSOR_HIDDEN)
    {
        if (window->wl.lockedPointer)
            unlockPointer(window);
    }

    if (window->cursorMode == GLFW_CURSOR_NORMAL)
    {
        if (cursor)
            setCursorImage(window, &cursor->wl);
        else
        {
            struct wl_cursor* defaultCursor =
                wl_cursor_theme_get_cursor(_glfw.wl.cursorTheme, "left_ptr");
            if (!defaultCursor)
            {
                _glfwInputError(GLFW_PLATFORM_ERROR,
                                "Wayland: Standard cursor not found");
                return;
            }

            struct wl_cursor* defaultCursorHiDPI = NULL;
            if (_glfw.wl.cursorThemeHiDPI)
            {
                defaultCursorHiDPI =
                    wl_cursor_theme_get_cursor(_glfw.wl.cursorThemeHiDPI, "left_ptr");
            }

            _GLFWcursorWayland cursorWayland =
            {
                defaultCursor,
                defaultCursorHiDPI,
                NULL,
                0, 0,
                0, 0,
                0
            };

            setCursorImage(window, &cursorWayland);
        }
    }
    else if (window->cursorMode == GLFW_CURSOR_HIDDEN ||
             window->cursorMode == GLFW_CURSOR_DISABLED)
    {
        wl_pointer_set_cursor(_glfw.wl.pointer, _glfw.wl.pointerEnterSerial, NULL, 0, 0);
    }
}

static void dataSourceHandleTarget(void* userData,
                                   struct wl_data_source* source,
                                   const char* mimeType)
{
    if (_glfw.wl.selectionSource != source)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Unknown clipboard data source");
        return;
    }
}

static void dataSourceHandleSend(void* userData,
                                 struct wl_data_source* source,
                                 const char* mimeType,
                                 int fd)
{
    // Ignore it if this is an outdated or invalid request
    if (_glfw.wl.selectionSource != source ||
        strcmp(mimeType, "text/plain;charset=utf-8") != 0)
    {
        close(fd);
        return;
    }

    char* string = _glfw.wl.clipboardString;
    size_t length = strlen(string);

    while (length > 0)
    {
        const ssize_t result = write(fd, string, length);
        if (result == -1)
        {
            if (errno == EINTR)
                continue;

            _glfwInputError(GLFW_PLATFORM_ERROR,
                            "Wayland: Error while writing the clipboard: %s",
                            strerror(errno));
            break;
        }

        length -= result;
        string += result;
    }

    close(fd);
}

static void dataSourceHandleCancelled(void* userData,
                                      struct wl_data_source* source)
{
    wl_data_source_destroy(source);

    if (_glfw.wl.selectionSource != source)
        return;

    _glfw.wl.selectionSource = NULL;
}

static const struct wl_data_source_listener dataSourceListener =
{
    dataSourceHandleTarget,
    dataSourceHandleSend,
    dataSourceHandleCancelled,
};

void _glfwPlatformSetClipboardString(const char* string)
{
    if (_glfw.wl.selectionSource)
    {
        wl_data_source_destroy(_glfw.wl.selectionSource);
        _glfw.wl.selectionSource = NULL;
    }

    char* copy = _glfw_strdup(string);
    if (!copy)
    {
        _glfwInputError(GLFW_OUT_OF_MEMORY, NULL);
        return;
    }

    free(_glfw.wl.clipboardString);
    _glfw.wl.clipboardString = copy;

    _glfw.wl.selectionSource =
        wl_data_device_manager_create_data_source(_glfw.wl.dataDeviceManager);
    if (!_glfw.wl.selectionSource)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to create clipboard data source");
        return;
    }
    wl_data_source_add_listener(_glfw.wl.selectionSource,
                                &dataSourceListener,
                                NULL);
    wl_data_source_offer(_glfw.wl.selectionSource, "text/plain;charset=utf-8");
    wl_data_device_set_selection(_glfw.wl.dataDevice,
                                 _glfw.wl.selectionSource,
                                 _glfw.wl.serial);
}

const char* _glfwPlatformGetClipboardString(void)
{
    if (!_glfw.wl.selectionOffer)
    {
        _glfwInputError(GLFW_FORMAT_UNAVAILABLE,
                        "Wayland: No clipboard data available");
        return NULL;
    }

    if (_glfw.wl.selectionSource)
        return _glfw.wl.clipboardString;

    free(_glfw.wl.clipboardString);
    _glfw.wl.clipboardString =
        readDataOfferAsString(_glfw.wl.selectionOffer, "text/plain;charset=utf-8");
    return _glfw.wl.clipboardString;
}

void _glfwPlatformGetRequiredInstanceExtensions(char** extensions)
{
    if (!_glfw.vk.KHR_surface || !_glfw.vk.KHR_wayland_surface)
        return;

    extensions[0] = "VK_KHR_surface";
    extensions[1] = "VK_KHR_wayland_surface";
}

int _glfwPlatformGetPhysicalDevicePresentationSupport(VkInstance instance,
                                                      VkPhysicalDevice device,
                                                      uint32_t queuefamily)
{
    PFN_vkGetPhysicalDeviceWaylandPresentationSupportKHR
        vkGetPhysicalDeviceWaylandPresentationSupportKHR =
        (PFN_vkGetPhysicalDeviceWaylandPresentationSupportKHR)
        vkGetInstanceProcAddr(instance, "vkGetPhysicalDeviceWaylandPresentationSupportKHR");
    if (!vkGetPhysicalDeviceWaylandPresentationSupportKHR)
    {
        _glfwInputError(GLFW_API_UNAVAILABLE,
                        "Wayland: Vulkan instance missing VK_KHR_wayland_surface extension");
        return VK_NULL_HANDLE;
    }

    return vkGetPhysicalDeviceWaylandPresentationSupportKHR(device,
                                                            queuefamily,
                                                            _glfw.wl.display);
}

VkResult _glfwPlatformCreateWindowSurface(VkInstance instance,
                                          _GLFWwindow* window,
                                          const VkAllocationCallbacks* allocator,
                                          VkSurfaceKHR* surface)
{
    VkResult err;
    VkWaylandSurfaceCreateInfoKHR sci;
    PFN_vkCreateWaylandSurfaceKHR vkCreateWaylandSurfaceKHR;

    vkCreateWaylandSurfaceKHR = (PFN_vkCreateWaylandSurfaceKHR)
        vkGetInstanceProcAddr(instance, "vkCreateWaylandSurfaceKHR");
    if (!vkCreateWaylandSurfaceKHR)
    {
        _glfwInputError(GLFW_API_UNAVAILABLE,
                        "Wayland: Vulkan instance missing VK_KHR_wayland_surface extension");
        return VK_ERROR_EXTENSION_NOT_PRESENT;
    }

    memset(&sci, 0, sizeof(sci));
    sci.sType = VK_STRUCTURE_TYPE_WAYLAND_SURFACE_CREATE_INFO_KHR;
    sci.display = _glfw.wl.display;
    sci.surface = window->wl.surface;

    err = vkCreateWaylandSurfaceKHR(instance, &sci, allocator, surface);
    if (err)
    {
        _glfwInputError(GLFW_PLATFORM_ERROR,
                        "Wayland: Failed to create Vulkan surface: %s",
                        _glfwGetVulkanResultString(err));
    }

    return err;
}


//////////////////////////////////////////////////////////////////////////
//////                        GLFW native API                       //////
//////////////////////////////////////////////////////////////////////////

GLFWAPI struct wl_display* glfwGetWaylandDisplay(void)
{
    _GLFW_REQUIRE_INIT_OR_RETURN(NULL);
    return _glfw.wl.display;
}

GLFWAPI struct wl_surface* glfwGetWaylandWindow(GLFWwindow* handle)
{
    _GLFWwindow* window = (_GLFWwindow*) handle;
    _GLFW_REQUIRE_INIT_OR_RETURN(NULL);
    return window->wl.surface;
}

