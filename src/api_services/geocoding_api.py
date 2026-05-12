from geopy.geocoders import (
    Nominatim
)

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
# GEOCODING API
# --------------------------------

def get_coordinates(location_name):

    try:

        geolocator = Nominatim(
            user_agent="landslide_prediction_system"
        )

        location = geolocator.geocode(

            location_name,

            timeout=10
        )

        if location is None:

            return None

        return {

            "latitude":
            location.latitude,

            "longitude":
            location.longitude,

            "address":
            location.address
        }

    except Exception as e:

        api_logger.error(
            f"Geocoding API Error: {e}"
        )

        return None