import requests
from app.core.error_codes import ErrorCode
from app.core.config import settings

# Load API key
WEATHER_API_KEY = settings.WEATHER_API_KEY
WEATHER_API_URL = settings.WEATHER_API_URL

class WeatherService:
    """
    Handles weather data retrieval from WeatherAPI.com.
    """

    @staticmethod
    def get_weather(location: str, parameters: list = None) -> dict:
        """
        Fetches weather data for the given location.

        :param location: The location (city, coordinates, etc.).
        :param parameters: Optional list of weather attributes to extract.
        :return: JSON with requested weather details.
        """

        if not WEATHER_API_KEY:
            return {
                "error": "Weather API key is missing.",
                "error_code": ErrorCode.INTERNAL_ERROR.value
            }

        params = {
            "key": WEATHER_API_KEY,
            "q": location,
            "aqi": "no"  # Disable air quality index for efficiency
        }

        try:
            response = requests.get(WEATHER_API_URL, params=params)
            if response.status_code != 200:
                return {
                    "error": f"Weather API error: {response.status_code}",
                    "error_code": ErrorCode.INTERNAL_ERROR.value
                }

            data = response.json()

            # Extract necessary weather data
            weather_data = {
                "location": data["location"]["name"],
                "region": data["location"]["region"],
                "country": data["location"]["country"],
                "last_updated": data["current"]["last_updated"],
            }

            available_params = {
                "temperature_c": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "humidity": data["current"]["humidity"],
                "wind_speed_kph": data["current"]["wind_kph"],
                "feels_like_c": data["current"]["feelslike_c"],
                "cloud_cover": data["current"]["cloud"]
            }

            # Filter requested parameters if provided
            if parameters:
                weather_data["weather"] = {
                    param: available_params[param] for param in parameters if param in available_params
                }
            else:
                weather_data["weather"] = available_params

            return weather_data

        except Exception as e:
            return {
                "error": f"Failed to fetch weather: {str(e)}",
                "error_code": ErrorCode.INTERNAL_ERROR.value
            }
