from app.services.query_generators.weather_query import WeatherQueryGenerator
from app.core.enums import Tag

class QueryFactory:
    """
    Factory class to dynamically select the correct query generator.
    """

    @staticmethod
    def get_query_generator(tag: str):
        if tag == Tag.WEATHER.value:
            return WeatherQueryGenerator()
        else:
            return None
