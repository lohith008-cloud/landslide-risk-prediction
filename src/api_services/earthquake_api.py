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
# EARTHQUAKE API
# --------------------------------

def get_earthquake(lat, lon):

    try:

        url = (
            "https://earthquake.usgs.gov/"
            "fdsnws/event/1/query"
        )

        params = {

            "format": "geojson",

            "latitude": lat,

            "longitude": lon,

            "maxradiuskm": 100,

            "limit": 10
        }

        response = requests.get(

            url,

            params=params,

            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        earthquake_count = len(
            data["features"]
        )

        return {

            "Earthquake_Activity":
            1 if earthquake_count > 0 else 0
        }

    except Exception as e:

        api_logger.error(
            f"Earthquake API Error: {e}"
        )

        return {

            "Earthquake_Activity": 0
        }