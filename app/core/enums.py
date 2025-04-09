from enum import Enum

class Tag(Enum):
    WEATHER = "weather"
    NEWS = "news"
    GENERAL = "general"
    JOKE = "joke"
    STORY = "story"
    UNKNOWN = "unknown"

    @staticmethod
    def get_all_tags():
        """
        Returns all valid tags as a comma-separated string.
        """
        return ", ".join(tag.value for tag in Tag)

class UserType(str, Enum):
    KNOWN = "known"
    UNKNOWN = "unknown"

    def __str__(self):
        return self.value

class Country(str, Enum):
    US = "us"
    UK = "gb"
    CANADA = "ca"
    INDIA = "in"

    def __str__(self):
        return self.value

class Category(Enum):
    BUSINESS = "business"
    TECHNOLOGY = "technology"
    SPORTS = "sports"
    HEALTH = "health"
    POLITICS = "politics"

class DeliveryMethod(str, Enum):
    DESCRIPTION = "description"  # Default
    SUMMARY = "summary"
    BULLET_POINTS = "bullet_points"
    ONE_SENTENCE = "one_sentence"