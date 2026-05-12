import requests
import random

from app.utils.logger import (
    setup_logger
)

# --------------------------------
# LOGGER
# --------------------------------

api_logger = setup_logger(
    "api_errors",
    "api_errors.log"
)

# --------------------------------
# ELEVATION API
# --------------------------------

def get_elevation_data(lat, lon):

    try:

        url = (
            "https://api.open-elevation.com/"
            "api/v1/lookup"
        )

        params = {

            "locations":
            f"{lat},{lon}"
        }

        response = requests.get(

            url,

            params=params,

            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        elevation = data[
            "results"
        ][0]["elevation"]

        # --------------------------------
        # SLOPE SIMULATION
        # --------------------------------

        if elevation > 2000:

            slope_angle = random.randint(
                35,
                60
            )

        elif elevation > 1000:

            slope_angle = random.randint(
                20,
                40
            )

        else:

            slope_angle = random.randint(
                5,
                20
            )

        aspect = random.randint(
            50,
            250
        )

        return {

            "Elevation_m": elevation,

            "Slope_Angle": slope_angle,

            "Aspect": aspect
        }

    except Exception as e:

        api_logger.error(
            f"Elevation API Error: {e}"
        )

        return {

            "Elevation_m": 500,

            "Slope_Angle": 25,

            "Aspect": 180
        }