import requests
import os

from dotenv import load_dotenv

from app.utils.logger import (
    setup_logger
)

# --------------------------------
# LOAD ENV
# --------------------------------

load_dotenv()

API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)

# --------------------------------
# LOGGER
# --------------------------------

api_logger = setup_logger(
    "api_errors",
    "api_errors.log"
)

# --------------------------------
# WEATHER API
# --------------------------------

def get_weather(lat, lon):

    try:

        url = (
            "https://api.openweathermap.org/"
            "data/2.5/weather"
        )

        params = {

            "lat": lat,

            "lon": lon,

            "appid": API_KEY,

            "units": "metric"
        }

        response = requests.get(

            url,

            params=params,

            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        rainfall = 0

        if "rain" in data:

            rainfall = data["rain"].get(
                "1h",
                0
            )

        return {

            "Rainfall_mm": rainfall,

            "Temperature_C":
            data["main"]["temp"],

            "Humidity_percent":
            data["main"]["humidity"]
        }

    except Exception as e:

        api_logger.error(
            f"Weather API Error: {e}"
        )

        return {

            "Rainfall_mm": 0,

            "Temperature_C": 25,

            "Humidity_percent": 50
        }