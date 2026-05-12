import numpy as np

def create_features(df):

    # --------------------------------
    # Rainfall Based Features
    # --------------------------------

    df["Rainfall_Intensity"] = (
        df["Rainfall_7Day"] /
        (df["Rainfall_3Day"] + 1)
    )

    df["Rainfall_Slope_Interaction"] = (
        df["Rainfall_mm"] *
        df["Slope_Angle"]
    )

    df["Rainfall_Humidity_Index"] = (
        df["Rainfall_mm"] *
        df["Humidity_percent"]
    )

    # --------------------------------
    # Terrain Features
    # --------------------------------

    df["Terrain_Risk"] = (
        df["Slope_Angle"] *
        df["Elevation_m"]
    )

    df["Elevation_Aspect_Risk"] = (
        df["Elevation_m"] *
        np.cos(
            np.radians(df["Aspect"])
        )
    )

    # --------------------------------
    # Vegetation Features
    # --------------------------------

    df["Vegetation_Loss_Index"] = (
        1 - df["NDVI_Index"]
    )

    df["Vegetation_Soil_Interaction"] = (
        df["NDVI_Index"] *
        df["Soil_Saturation"]
    )

    # --------------------------------
    # Water Influence Features
    # --------------------------------

    df["Water_Proximity_Risk"] = (
        1 /
        (df["Proximity_to_Water"] + 1)
    )

    # --------------------------------
    # Road Instability Features
    # --------------------------------

    df["Road_Risk"] = (
        1 /
        (df["Distance_to_Road_m"] + 1)
    )

    # --------------------------------
    # Earthquake Influence
    # --------------------------------

    df["Seismic_Terrain_Risk"] = (
        df["Earthquake_Activity"] *
        df["Slope_Angle"]
    )

    # --------------------------------
    # Combined Environmental Risk
    # --------------------------------

    df["Combined_Risk_Index"] = (

        df["Rainfall_mm"] *

        df["Slope_Angle"] *

        (1 - df["NDVI_Index"])
    )

    return df