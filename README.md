<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=13&pause=1000&color=FF6B6B&center=true&vCenter=true&width=435&lines=Real-time+Landslide+Risk+Assessment" alt="Typing SVG" />

# 🏔️ Landslide Risk Prediction System

**An end-to-end machine learning system for real-time landslide susceptibility assessment powered by satellite data, live weather APIs, and an ensemble ML model.**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-landslide--risk--prediction.onrender.com-FF6B6B?style=for-the-badge&logoColor=white)](https://landslide-risk-prediction.onrender.com)

---

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-189F47?style=flat-square)](https://xgboost.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com)

</div>

---

## 📌 Overview

The **Landslide Risk Prediction System** combines geospatial APIs, satellite-derived vegetation indices, seismic data, and a trained ensemble classifier to deliver instant landslide risk scores for any coordinate on Earth. Users can input a location manually or let the system pull live data from five external APIs — no GIS expertise required.

> **Use case:** Early warning for disaster management agencies, civil engineers, trekkers, and researchers operating in landslide-prone regions.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **Risk Prediction** | Probability score + 5-tier risk category (Very Low → Very High) |
| 🌧️ **Live Weather** | Real-time rainfall, humidity & soil moisture via OpenWeatherMap |
| 🏔️ **Terrain Analysis** | Elevation, slope, aspect, curvature & TPI via Open-Elevation |
| 🌿 **Vegetation Index** | NDVI from NASA MODIS satellite composites |
| 🌋 **Seismic Activity** | Recent earthquake data from USGS Earthquake API |
| 📍 **Geocoding** | Forward/reverse geocoding via OpenStreetMap Nominatim |
| 📊 **Analytics Dashboard** | Prediction history, risk trends & feature importance charts |
| 🧠 **In-App Training** | Train the ML model directly from the Streamlit UI |
| 📋 **JSON Export** | Full structured prediction report per location |

---

## 🖥️ Live Demo

> 🔗 **[https://landslide-risk-prediction.onrender.com](https://landslide-risk-prediction.onrender.com)**

<div align="center">

| Page | Description |
|---|---|
| **🎯 Predict Risk** | Enter coordinates or place name → get instant risk assessment |
| **🧠 Train Model** | Configure & train the ensemble model with live progress tracking |
| **📊 Analytics** | View prediction history, feature radar & importance charts |
| **⚙️ Settings** | Manage API keys, thresholds & read documentation |

</div>

---

## 🏗️ Architecture

```
landslide_project/
│
├── app/
│   └── app.py                   # Streamlit multi-page frontend
│
├── src/
│   ├── data_ingestion.py        # NASA GLC download + synthetic generation
│   ├── data_preprocessing.py    # Cleaning, validation, outlier removal
│   ├── feature_engineering.py   # Feature creation, encoding & scaling
│   ├── train_model.py           # Ensemble training pipeline
│   ├── evaluate_model.py        # Metrics, ROC/PR curves, confusion matrix
│   ├── predict_pipeline.py      # End-to-end prediction orchestration
│   └── api_services/
│       ├── weather_api.py       # OpenWeatherMap integration
│       ├── elevation_api.py     # Open-Elevation / OpenTopoData
│       ├── ndvi_api.py          # NASA MODIS NDVI
│       ├── earthquake_api.py    # USGS Earthquake Hazards API
│       └── geocoding_api.py     # Nominatim / OpenStreetMap
│
├── config/
│   └── config.yaml              # API keys, thresholds, model settings
│
├── models/                      # Saved .pkl artifacts (post-training)
├── data/                        # raw/ · processed/ · external/
├── logs/                        # training.log · prediction.log · api_errors.log
├── main.py                      # Entry point → launches Streamlit
└── requirements.txt
```

---

## 🤖 Machine Learning Pipeline

### Model
A **soft-voting ensemble** of three classifiers trained on landslide-prone feature distributions:

| Estimator | Weight | Role |
|---|---|---|
| Random Forest | 3 | Handles non-linear boundaries, robust to noise |
| Gradient Boosting | 2 | Sequential error correction |
| XGBoost | 3 | Fast, regularised boosting |

### Feature Engineering
Beyond raw inputs, the model uses eight derived features:

| Engineered Feature | Formula / Description |
|---|---|
| `rain_slope_interaction` | `rainfall × slope / 100` |
| `rain_soil_moisture_product` | `rainfall × soil_moisture` |
| `topographic_wetness_index` | `ln(catchment_area / tan(slope))` |
| `vegetation_protection_score` | `1 − NDVI` |
| `seismic_slope_risk` | `magnitude × slope / ln(1 + dist_fault)` |
| `slope_stability_index` | Simplified Newmark displacement proxy |
| `normalized_rainfall_intensity` | Rainfall normalised by log-elevation |
| `combined_trigger_index` | Weighted composite of all triggers |

### Training Details
- **Class balancing:** SMOTE oversampling
- **Validation:** 5-fold Stratified K-Fold
- **Typical CV ROC-AUC:** `0.93 – 0.97`

---

## 🔌 External APIs

| API | Provider | Auth Required | Data Provided |
|---|---|---|---|
| Weather | [OpenWeatherMap](https://openweathermap.org/api) | ✅ Free key | Rainfall, humidity, wind, pressure |
| Elevation | [Open-Elevation](https://open-elevation.com) | ❌ None | Elevation grid → slope, aspect, curvature |
| NDVI | [NASA MODIS ORNL](https://modis.ornl.gov) | ✅ Free account | 250 m vegetation index (16-day composite) |
| Earthquake | [USGS](https://earthquake.usgs.gov/fdsnws/event/1/) | ❌ None | Magnitude, depth, epicentre distance |
| Geocoding | [Nominatim / OSM](https://nominatim.openstreetmap.org) | ❌ None | Address ↔ coordinates |

---

## ⚡ Local Setup

### 1 — Clone the Repository
```bash
git clone https://github.com/your-username/landslide-prediction-system.git
cd landslide-prediction-system
```

### 2 — Create Virtual Environment
```bash
# Windows
python -m venv myvenv
myvenv\Scripts\activate

# macOS / Linux
python -m venv myvenv
source myvenv/bin/activate
```

### 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### 4 — Configure API Keys
Open `config/config.yaml` and add your keys:
```yaml
api_keys:
  openweather: "YOUR_OPENWEATHERMAP_KEY"      # openweathermap.org/api (free tier)
  nasa_earthdata_username: "YOUR_USERNAME"     # urs.earthdata.nasa.gov (free)
  nasa_earthdata_password: "YOUR_PASSWORD"
```
> **Note:** Elevation, Earthquake, and Geocoding APIs require no keys.

### 5 — Launch the App
```bash
python main.py
# Opens at → http://localhost:8501
```

---

## 🧪 CLI Usage

Always run from the **project root** directory:

```bash
# Train the model from command line
python -m src.train_model

# Run a test prediction
python -m src.predict_pipeline

# Run preprocessing only
python -m src.data_preprocessing
```

> ⚠️ **Common mistake:** Running `python src/train_model.py` from inside the `src/` folder causes `ModuleNotFoundError: No module named 'src'`.  
> ✅ **Fix:** Always use `python -m src.module_name` from the project root.

---

## 🎯 Risk Categories

| Level | Probability | Indicator | Recommended Action |
|---|---|---|---|
| 🔴 Very High | ≥ 80% | Critical | **Evacuate immediately** |
| 🟠 High | 60 – 80% | Danger | Prepare for evacuation |
| 🟡 Moderate | 40 – 60% | Caution | Stay alert, monitor alerts |
| 🟢 Low | 20 – 40% | Advisory | Normal precautions |
| ✅ Very Low | < 20% | Safe | Conditions stable |

---

## 📦 Dependencies

```
streamlit          plotly             scikit-learn
xgboost            lightgbm           imbalanced-learn
pandas             numpy              joblib
requests           pyyaml             folium
streamlit-folium   geopandas          rasterio
tenacity           loguru             python-dotenv
```

Full list: [`requirements.txt`](requirements.txt)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch — `git checkout -b feature/AmazingFeature`
3. Commit your changes — `git commit -m 'Add AmazingFeature'`
4. Push to the branch — `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 🙏 Acknowledgements

- [NASA Global Landslide Catalog](https://data.nasa.gov/Earth-Science/Global-Landslide-Catalog/dd9i-98ck) — Training data source
- [USGS Earthquake Hazards Program](https://earthquake.usgs.gov) — Real-time seismic data
- [OpenWeatherMap](https://openweathermap.org) — Weather data
- [OpenStreetMap / Nominatim](https://nominatim.openstreetmap.org) — Geocoding services
- [NASA ORNL DAAC](https://modis.ornl.gov) — MODIS NDVI products

---

<div align="center">

**Built with ❤️ for disaster risk reduction**

[![Live Demo](https://img.shields.io/badge/🚀%20Try%20Live%20Demo-FF6B6B?style=for-the-badge)](https://landslide-risk-prediction.onrender.com)

</div>
