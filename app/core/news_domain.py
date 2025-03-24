from enum import Enum

class NewsDomain(Enum):
    """
    Stores country-specific news domains.
    """
    GLOBAL = ["bbc", "cnn", "nytimes", "reuters"]
    US = ["nytimes", "cnn", "foxnews", "washingtonpost"]
    GB = ["bbc", "Givemesport"]
    FR = ["lemonde", "lefigaro", "20minutes"]

    @staticmethod
    def get_domains_for_country(country: str) -> list:
        """Returns the news domains for the given country, or a default list if not found."""
        domain_enum = getattr(NewsDomain, country.upper(), NewsDomain.GLOBAL)
        return domain_enum.value  # Extracts the actual list of domains
