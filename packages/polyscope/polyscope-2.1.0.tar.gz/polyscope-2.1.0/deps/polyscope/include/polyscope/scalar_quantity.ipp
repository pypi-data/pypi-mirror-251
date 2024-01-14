// Copyright 2017-2023, Nicholas Sharp and the Polyscope contributors. https://polyscope.run

#include "imgui.h"
#include "polyscope/utilities.h"
namespace polyscope {

template <typename QuantityT>
ScalarQuantity<QuantityT>::ScalarQuantity(QuantityT& quantity_, const std::vector<float>& values_, DataType dataType_)
    : quantity(quantity_), values(&quantity, quantity.uniquePrefix() + "values", valuesData), valuesData(values_),
      dataType(dataType_), dataRange(robustMinMax(values.data, 1e-5)),
      vizRangeMin(quantity.uniquePrefix() + "vizRangeMin", -777.), // set later,
      vizRangeMax(quantity.uniquePrefix() + "vizRangeMax", -777.), // including clearing cache
      cMap(quantity.uniquePrefix() + "cmap", defaultColorMap(dataType)),
      isolinesEnabled(quantity.uniquePrefix() + "isolinesEnabled", false),
      isolineWidth(quantity.uniquePrefix() + "isolineWidth",
                   absoluteValue((dataRange.second - dataRange.first) * 0.02)),
      isolineDarkness(quantity.uniquePrefix() + "isolineDarkness", 0.7)

{
  hist.updateColormap(cMap.get());
  hist.buildHistogram(values.data);

  if (vizRangeMin.holdsDefaultValue()) { // min and max should always have same cache state
    // dynamically compute a viz range from the data min/max
    // note that this also clears the persistent value's cahce, so it's like it was never set
    resetMapRange();
  }
}

template <typename QuantityT>
void ScalarQuantity<QuantityT>::buildScalarUI() {

  if (render::buildColormapSelector(cMap.get())) {
    quantity.refresh();
    hist.updateColormap(cMap.get());
    setColorMap(getColorMap());
  }

  // Reset button
  ImGui::SameLine();
  if (ImGui::Button("Reset")) {
    resetMapRange();
  }


  // == Build the help box for the scalar quantity.
  std::string extraText = "";
  switch (dataType) {
  case DataType::STANDARD: {
  } break;
  case DataType::SYMMETRIC: {
    extraText = "This quantity was added as **symmetric** scalar quantity, so only a "
                "single symmetric range control can be adjusted.";
  } break;
  case DataType::MAGNITUDE: {
    extraText = "This quantity was added as **magnitude** scalar quantity, so only a "
                "single symmetric range control can be adjusted, and it must be positive.";
  } break;
  }
  ImGui::SameLine();
  ImGuiHelperMarker(("The window below shows the colormap used to visualize this scalar, "
                     "and a histogram of the the data values. The text boxes below show the "
                     "range limits for the color map."
                     "\n\n"
                     "To adjust the limit range for the color map, click-and-drag on the text "
                     "box. Control-click to type a value, even one outside the visible range." +
                     extraText)
                        .c_str());


  // Draw the histogram of values
  hist.colormapRange = std::pair<float, float>(vizRangeMin.get(), vizRangeMax.get());
  float windowWidth = ImGui::GetWindowWidth();
  float histWidth = 0.75 * windowWidth;
  hist.buildUI(histWidth);

  // Data range
  // Note: %g specifiers are generally nicer than %e, but here we don't acutally have a choice. ImGui (for somewhat
  // valid reasons) links the resolution of the slider to the decimal width of the formatted number. When %g formats a
  // number with few decimal places, sliders can break. There is no way to set a minimum number of decimal places with
  // %g, unfortunately.
  {

    float imPad = ImGui::GetStyle().ItemSpacing.x;
    ImGui::PushItemWidth((histWidth - imPad) / 2);
    float speed = (dataRange.second - dataRange.first) / 100.;
    bool changed = false;

    switch (dataType) {
    case DataType::STANDARD: {

      changed = changed || ImGui::DragFloat("##min", &vizRangeMin.get(), speed, dataRange.first, vizRangeMax.get(),
                                            "%.5g", ImGuiSliderFlags_NoRoundToFormat);
      ImGui::SameLine();
      changed = changed || ImGui::DragFloat("##max", &vizRangeMax.get(), speed, vizRangeMin.get(), dataRange.second,
                                            "%.5g", ImGuiSliderFlags_NoRoundToFormat);

    } break;
    case DataType::SYMMETRIC: {
      float absRange = std::max(std::abs(dataRange.first), std::abs(dataRange.second));

      if (ImGui::DragFloat("##min", &vizRangeMin.get(), speed, -absRange, 0.f, "%.5g",
                           ImGuiSliderFlags_NoRoundToFormat)) {
        vizRangeMax.get() = -vizRangeMin.get();
        changed = true;
      }
      ImGui::SameLine();
      if (ImGui::DragFloat("##max", &vizRangeMax.get(), speed, 0.f, absRange, "%.5g",
                           ImGuiSliderFlags_NoRoundToFormat)) {
        vizRangeMin.get() = -vizRangeMax.get();
        changed = true;
      }

    } break;
    case DataType::MAGNITUDE: {
      changed = changed || ImGui::DragFloat("##max", &vizRangeMax.get(), speed, 0.f, dataRange.second, "%.5g",
                                            ImGuiSliderFlags_NoRoundToFormat);

    } break;
    }

    if (changed) {
      vizRangeMin.manuallyChanged();
      vizRangeMax.manuallyChanged();
      requestRedraw();
    }

    ImGui::PopItemWidth();
  }

  // Isolines
  if (isolinesEnabled.get()) {
    ImGui::PushItemWidth(100);

    // Isoline width
    ImGui::TextUnformatted("Isoline width");
    ImGui::SameLine();
    if (isolineWidth.get().isRelative()) {
      if (ImGui::DragFloat("##Isoline width relative", isolineWidth.get().getValuePtr(), .001, 0.0001, 1.0, "%.4f",
                           ImGuiSliderFlags_Logarithmic | ImGuiSliderFlags_NoRoundToFormat)) {
        isolineWidth.manuallyChanged();
        requestRedraw();
      }
    } else {
      float scaleWidth = dataRange.second - dataRange.first;
      if (ImGui::DragFloat("##Isoline width absolute", isolineWidth.get().getValuePtr(), scaleWidth / 1000, 0.,
                           scaleWidth, "%.4f", ImGuiSliderFlags_Logarithmic | ImGuiSliderFlags_NoRoundToFormat)) {
        isolineWidth.manuallyChanged();
        requestRedraw();
      }
    }

    // Isoline darkness
    ImGui::TextUnformatted("Isoline darkness");
    ImGui::SameLine();
    if (ImGui::DragFloat("##Isoline darkness", &isolineDarkness.get(), 0.01, 0.)) {
      isolineDarkness.manuallyChanged();
      requestRedraw();
    }

    ImGui::PopItemWidth();
  }
}

template <typename QuantityT>
void ScalarQuantity<QuantityT>::buildScalarOptionsUI() {
  if (ImGui::MenuItem("Reset colormap range")) resetMapRange();
  if (ImGui::MenuItem("Enable isolines", NULL, isolinesEnabled.get())) setIsolinesEnabled(!isolinesEnabled.get());
}

template <typename QuantityT>
std::vector<std::string> ScalarQuantity<QuantityT>::addScalarRules(std::vector<std::string> rules) {
  rules.push_back("SHADE_COLORMAP_VALUE");
  if (isolinesEnabled.get()) {
    rules.push_back("ISOLINE_STRIPE_VALUECOLOR");
  }
  return rules;
}


template <typename QuantityT>
void ScalarQuantity<QuantityT>::setScalarUniforms(render::ShaderProgram& p) {
  p.setUniform("u_rangeLow", vizRangeMin.get());
  p.setUniform("u_rangeHigh", vizRangeMax.get());

  if (isolinesEnabled.get()) {
    p.setUniform("u_modLen", getIsolineWidth());
    p.setUniform("u_modDarkness", getIsolineDarkness());
  }
}

template <typename QuantityT>
QuantityT* ScalarQuantity<QuantityT>::resetMapRange() {
  switch (dataType) {
  case DataType::STANDARD:
    vizRangeMin = dataRange.first;
    vizRangeMax = dataRange.second;
    break;
  case DataType::SYMMETRIC: {
    double absRange = std::max(std::abs(dataRange.first), std::abs(dataRange.second));
    vizRangeMin = -absRange;
    vizRangeMax = absRange;
  } break;
  case DataType::MAGNITUDE:
    vizRangeMin = 0.;
    vizRangeMax = dataRange.second;
    break;
  }

  vizRangeMin.clearCache();
  vizRangeMax.clearCache();

  requestRedraw();
  return &quantity;
}

template <typename QuantityT>
template <class V>
void ScalarQuantity<QuantityT>::updateData(const V& newValues) {
  validateSize(newValues, values.size(), "scalar quantity " + quantity.name);
  values.data = standardizeArray<float, V>(newValues);
  values.markHostBufferUpdated();
}


template <typename QuantityT>
QuantityT* ScalarQuantity<QuantityT>::setColorMap(std::string val) {
  cMap = val;
  hist.updateColormap(cMap.get());
  quantity.refresh();
  requestRedraw();
  return &quantity;
}
template <typename QuantityT>
std::string ScalarQuantity<QuantityT>::getColorMap() {
  return cMap.get();
}

template <typename QuantityT>
QuantityT* ScalarQuantity<QuantityT>::setMapRange(std::pair<double, double> val) {
  vizRangeMin = val.first;
  vizRangeMax = val.second;
  requestRedraw();
  return &quantity;
}
template <typename QuantityT>
std::pair<double, double> ScalarQuantity<QuantityT>::getMapRange() {
  return std::pair<float, float>(vizRangeMin.get(), vizRangeMax.get());
}
template <typename QuantityT>
std::pair<double, double> ScalarQuantity<QuantityT>::getDataRange() {
  return dataRange;
}

template <typename QuantityT>
QuantityT* ScalarQuantity<QuantityT>::setIsolineWidth(double size, bool isRelative) {
  isolineWidth = ScaledValue<float>(size, isRelative);
  if (!isolinesEnabled.get()) {
    setIsolinesEnabled(true);
  }
  requestRedraw();
  return &quantity;
}
template <typename QuantityT>
double ScalarQuantity<QuantityT>::getIsolineWidth() {
  return isolineWidth.get().asAbsolute();
}

template <typename QuantityT>
QuantityT* ScalarQuantity<QuantityT>::setIsolineDarkness(double val) {
  isolineDarkness = val;
  if (!isolinesEnabled.get()) {
    setIsolinesEnabled(true);
  }
  requestRedraw();
  return &quantity;
}
template <typename QuantityT>
double ScalarQuantity<QuantityT>::getIsolineDarkness() {
  return isolineDarkness.get();
}

template <typename QuantityT>
QuantityT* ScalarQuantity<QuantityT>::setIsolinesEnabled(bool newEnabled) {
  isolinesEnabled = newEnabled;
  quantity.refresh();
  requestRedraw();
  return &quantity;
}
template <typename QuantityT>
bool ScalarQuantity<QuantityT>::getIsolinesEnabled() {
  return isolinesEnabled.get();
}

} // namespace polyscope
