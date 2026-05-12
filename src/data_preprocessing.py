import numpy as np
import pandas as pd

FEATURES = [

    # Original Features

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

    # Engineered Features

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

TARGET = "Label"

def preprocess_data(df):

    # --------------------------------
    # Remove Duplicate Rows
    # --------------------------------

    df = df.drop_duplicates()

    # --------------------------------
    # Replace Infinite Values
    # --------------------------------

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # --------------------------------
    # Fill Missing Values
    # --------------------------------

    df = df.fillna(
        df.median(numeric_only=True)
    )

    # --------------------------------
    # Ensure Numeric Datatypes
    # --------------------------------

    for column in FEATURES:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # --------------------------------
    # Fill Remaining NaNs
    # --------------------------------

    df = df.fillna(0)

    # --------------------------------
    # Basic Outlier Clipping
    # --------------------------------

    for column in FEATURES:

        lower_limit = df[column].quantile(0.01)

        upper_limit = df[column].quantile(0.99)

        df[column] = df[column].clip(
            lower_limit,
            upper_limit
        )

    # --------------------------------
    # Final Feature Selection
    # --------------------------------

    X = df[FEATURES]

    y = df[TARGET]

    return X, y