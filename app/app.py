import sys
import os

# --------------------------------
# PROJECT ROOT PATH FIX
# --------------------------------

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, project_root)

# --------------------------------
# IMPORTS
# --------------------------------

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import joblib

from src.predict_pipeline import (
    predict_landslide
)

from src.api_services.geocoding_api import (
    get_coordinates
)

from src.api_services.weather_api import (
    get_weather
)

from src.api_services.elevation_api import (
    get_elevation_data
)

from src.api_services.ndvi_api import (
    get_ndvi
)

from src.api_services.earthquake_api import (
    get_earthquake
)

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(

    page_title="Landslide Prediction System",

    page_icon="🌍",

    layout="wide"
)

# --------------------------------
# LOAD MODEL
# --------------------------------

model = joblib.load(
    "models/landslide_model.pkl"
)

# --------------------------------
# TITLE
# --------------------------------

st.title(
    "🌍 Real-Time Landslide Prediction System"
)

st.markdown(
    """
    Predict landslide risk using:
    
    - Weather conditions
    - Terrain analysis
    - Vegetation analysis
    - Earthquake activity
    - Real-time environmental APIs
    """
)

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.header(
    "Prediction Inputs"
)

location = st.sidebar.text_input(

    "Enter Location",

    placeholder="Hyderabad"
)

soil = st.sidebar.selectbox(

    "Soil Saturation",

    ["Dry", "Moist", "Wet"]
)

vegetation = st.sidebar.selectbox(

    "Vegetation Density",

    ["Sparse", "Moderate", "Dense"]
)

# --------------------------------
# PREDICTION BUTTON
# --------------------------------

if st.sidebar.button(
    "Predict Landslide Risk"
):

    # --------------------------------
    # FETCH ENVIRONMENTAL DATA
    # --------------------------------

    with st.spinner(
        "Fetching environmental data..."
    ):

        coords = get_coordinates(
            location
        )

        if coords is None:

            st.error(
                "Invalid Location"
            )

            st.stop()

        weather = get_weather(

            coords["latitude"],

            coords["longitude"]
        )

        elevation = get_elevation_data(

            coords["latitude"],

            coords["longitude"]
        )

        ndvi = get_ndvi(

            coords["latitude"],

            coords["longitude"]
        )

        earthquake = get_earthquake(

            coords["latitude"],

            coords["longitude"]
        )

    # --------------------------------
    # INPUT ENCODING
    # --------------------------------

    soil_map = {

        "Dry": 0.2,

        "Moist": 0.5,

        "Wet": 0.9
    }

    vegetation_map = {

        "Sparse": 0.2,

        "Moderate": 0.5,

        "Dense": 0.8
    }

    # --------------------------------
    # CREATE MODEL INPUT
    # --------------------------------

    runtime_data = {

        "Rainfall_mm":
        weather["Rainfall_mm"],

        "Slope_Angle":
        elevation["Slope_Angle"],

        "Soil_Saturation":
        soil_map[soil],

        "Vegetation_Cover":
        vegetation_map[vegetation],

        "Rainfall_3Day":
        weather["Rainfall_mm"] * 3,

        "Rainfall_7Day":
        weather["Rainfall_mm"] * 7,

        "Aspect":
        elevation["Aspect"],

        "Elevation_m":
        elevation["Elevation_m"],

        "NDVI_Index":
        ndvi["NDVI_Index"],

        "Land_Use_Urban": 0,

        "Land_Use_Forest": 1,

        "Land_Use_Agriculture": 0,

        "Earthquake_Activity":
        earthquake["Earthquake_Activity"],

        "Proximity_to_Water": 0.5,

        "Distance_to_Road_m": 200,

        "Temperature_C":
        weather["Temperature_C"],

        "Humidity_percent":
        weather["Humidity_percent"]
    }

    # --------------------------------
    # MODEL PREDICTION
    # --------------------------------
    result = predict_landslide(
        runtime_data,
        coords["address"]
    )

    # --------------------------------
    # METRICS
    # --------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Risk Level",

        result["risk"]
    )

    col2.metric(

        "Probability",

        f'{result["probability"]}%'
    )

    col3.metric(

        "Temperature",

        f'{weather["Temperature_C"]} °C'
    )

    # --------------------------------
    # GAUGE CHART
    # --------------------------------

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=result["probability"],

        title={
            'text': "Landslide Probability"
        },

        gauge={
            'axis': {'range': [0, 100]}
        }
    ))

    st.plotly_chart(

        fig,

        use_container_width=True
    )

    # --------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------

    feature_names = [

        "Rainfall_mm",
        "Slope_Angle",
        "Soil_Saturation",
        "Vegetation_Cover",
        "Rainfall_3Day",
        "Rainfall_7Day",
        "Aspect",
        "Elevation_m",
        "NDVI_Index",
        "Land_Use_Urban",
        "Land_Use_Forest",
        "Land_Use_Agriculture",
        "Earthquake_Activity",
        "Proximity_to_Water",
        "Distance_to_Road_m",
        "Temperature_C",
        "Humidity_percent",

        "Rainfall_Intensity",
        "Rainfall_Slope_Interaction",
        "Rainfall_Humidity_Index",
        "Terrain_Risk",
        "Elevation_Aspect_Risk",
        "Vegetation_Loss_Index",
        "Vegetation_Soil_Interaction",
        "Water_Proximity_Risk",
        "Road_Risk",
        "Seismic_Terrain_Risk",
        "Combined_Risk_Index"
    ]

    feature_importance = pd.DataFrame({

        "Feature": feature_names,

        "Importance":
        model.named_steps[
            "model"
        ].feature_importances_
    })

    feature_importance = feature_importance.sort_values(

        by="Importance",

        ascending=False
    )

    st.subheader(
        "📊 Feature Importance"
    )

    st.bar_chart(
        feature_importance.set_index(
            "Feature"
        )
    )

    # --------------------------------
    # LOCATION
    # --------------------------------

    st.subheader(
        "📍 Location"
    )

    st.info(
        coords["address"]
    )

    # --------------------------------
    # WEATHER DATA
    # --------------------------------

    st.subheader(
        "🌦 Weather Data"
    )

    st.json(weather)

    # --------------------------------
    # TERRAIN DATA
    # --------------------------------

    st.subheader(
        "⛰ Terrain Data"
    )

    st.json(elevation)

    # --------------------------------
    # NDVI DATA
    # --------------------------------

    st.subheader(
        "🌱 Vegetation Analysis"
    )

    st.json(ndvi)

    # --------------------------------
    # EARTHQUAKE DATA
    # --------------------------------

    st.subheader(
        "🌍 Earthquake Activity"
    )

    st.json(earthquake)

    # --------------------------------
    # SAFETY RECOMMENDATIONS
    # --------------------------------

    st.subheader(
        "⚠ Safety Recommendations"
    )

    if result["risk"] == "HIGH RISK":

        st.error(
            """
            Avoid landslide-prone areas.

            Avoid travel in hilly regions.

            Monitor weather alerts continuously.
            """
        )

    elif result["risk"] == "MEDIUM RISK":

        st.warning(
            """
            Travel carefully in elevated terrain.

            Monitor rainfall conditions.
            """
        )

    else:

        st.success(
            """
            Current environmental conditions appear safer.
            """
        )