import pandas as pd
import joblib

from src.feature_engineering import (
    create_features
)

from app.utils.logger import (
    setup_logger
)

# --------------------------------
# LOGGER
# --------------------------------

prediction_logger = setup_logger(
    "prediction",
    "prediction.log"
)

# --------------------------------
# LOAD MODEL
# --------------------------------

model = joblib.load(
    "models/landslide_model.pkl"
)

# --------------------------------
# PREDICTION FUNCTION
# --------------------------------

def predict_landslide(

    runtime_data,

    location_name=None
):

    # --------------------------------
    # CONVERT TO DATAFRAME
    # --------------------------------

    df = pd.DataFrame(
        [runtime_data]
    )

    # --------------------------------
    # FEATURE ENGINEERING
    # --------------------------------

    df = create_features(df)

    # --------------------------------
    # MODEL PREDICTION
    # --------------------------------

    prediction = model.predict(df)[0]

    probability = round(

        model.predict_proba(df)[0][1] * 100,

        2
    )

    # --------------------------------
    # RISK LEVEL
    # --------------------------------

    if probability >= 70:

        risk = "HIGH RISK"

    elif probability >= 40:

        risk = "MEDIUM RISK"

    else:

        risk = "LOW RISK"

    # --------------------------------
    # SAFETY STATUS
    # --------------------------------

    status = (

        "SAFE"

        if risk == "LOW RISK"

        else "UNSAFE"
    )

    # --------------------------------
    # LOG PREDICTION
    # --------------------------------

    prediction_logger.info(

        f"\nPrediction Made\n\n"

        f"Location        : {location_name}\n"

        f"Risk Status     : {status}\n"

        f"Risk Level      : {risk}\n"

        f"Probability     : {probability:.2f}%\n\n"

        f"{'-'*40}"
    )

    # --------------------------------
    # RETURN RESULT
    # --------------------------------

    return {

        "risk": risk,

        "status": status,

        "probability": probability
    }