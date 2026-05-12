import requests

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
# NDVI API
# --------------------------------

def get_ndvi(lat, lon):

    try:

        url = (
            "https://api.open-meteo.com/"
            "v1/forecast"
        )

        params = {

            "latitude": lat,

            "longitude": lon,

            "current":
            "temperature_2m,relative_humidity_2m"
        }

        response = requests.get(

            url,

            params=params,

            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        temperature = data[
            "current"
        ]["temperature_2m"]

        humidity = data[
            "current"
        ]["relative_humidity_2m"]

        # --------------------------------
        # VEGETATION INDEX APPROXIMATION
        # --------------------------------

        ndvi = (
            (humidity / 100) * 0.6
        ) + (
            max(0, (35 - temperature)) / 35
        ) * 0.4

        ndvi = round(
            min(max(ndvi, 0.1), 0.9),
            2
        )

        return {

            "NDVI_Index": ndvi
        }

    except Exception as e:

        api_logger.error(
            f"NDVI API Error: {e}"
        )

        return {

            "NDVI_Index": 0.5
        }