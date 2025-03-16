from abc import ABC, abstractmethod

class BaseQueryGenerator(ABC):
    """
    Abstract base class for all query generators.
    Ensures every query follows a structured format.
    """

    @abstractmethod
    def generate_query(self, parsed_json: dict) -> str:
        """
        Converts structured JSON into an AI query string.
        Must be implemented by subclasses.
        """
        pass
