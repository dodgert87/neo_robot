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