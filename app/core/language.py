from enum import Enum

class Language(Enum):
    ENGLISH = "en"
    FRENCH = "fr"
    FINNISH = "fi"
    ARABIC = "ar"

    @classmethod
    def get_all_languages(cls):
        """
        Returns a comma-separated string of supported language codes.
        """
        return ", ".join([lang.value for lang in cls])
