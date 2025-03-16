from app.services.query_generators.base_query import BaseQueryGenerator
from app.services.weather_service import WeatherService
import json

class WeatherQueryGenerator(BaseQueryGenerator):
    """
    Generates AI query for weather-related requests.
    """

    def generate_query(self, parsed_json: dict) -> str:
        """
        Converts structured JSON into a formatted AI query.
        Handles weather data retrieval before formatting.
        """
        location = parsed_json["parameters"].get("location", "unknown location")

        # Fetch real-time weather data
        weather_data = WeatherService.get_weather(location)

        # Handle API error cases
        if "error" in weather_data:
            return f"Could not fetch weather for {location}. Reason: {weather_data['error']}"

        # Prepare the AI query payload
        ai_query = (
            f"Generate a natural and conversational response based on the following weather data:\n"
            f"{json.dumps(weather_data, indent=2)}\n\n"
            f"Context: The user asked the following: '{parsed_json['command']}'\n"
            f"Make it engaging, human-like, and easy to understand. dont include all the information if it is not requested and the context is you having a conversion with someone about the weather\n"
            f"dont assume that the person asking is in that location unless he mention that or you can infer it from the context\n"
            f"for wind speed and non key data like humidity use a relative reference not number"
        )

        return ai_query
