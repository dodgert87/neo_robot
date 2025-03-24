from newsdataapi import NewsDataApiClient
from app.core.enums import Country, Category
from app.core.news_domain import NewsDomain
from app.core.language import Language
from app.core.config import settings
from app.core.error_codes import ErrorCode

API_KEY = settings.NEWS_API_KEY


class NewsService:
    api_client = NewsDataApiClient(apikey=API_KEY)

    @staticmethod
    def _get_api_params(
        query: str = None,
        category: Category = None,
        language: Language = Language.ENGLISH,
        country: Country = Country.US,
        timeframe: str = None,
        sources: list = None
    ) -> dict:
        """Generates the API parameters dynamically."""
        params = {
            "language": language.value,
            "country": country.value,
            "size": 10,  # Limit results to 10
            "image": False,  # Ensure it's a boolean
            "full_content": False,  # Exclude full article content
            "removeduplicate": True,  # Remove duplicates
        }

        if query:
            params["q"] = query
        if category:
            params["category"] = category.value
        if timeframe:
            params["timeframe"] = timeframe  # Ensure timeframe is correctly formatted

        # Handle domain filtering dynamically (prioritizing user-specified sources)
        if sources and isinstance(sources, list):
            params["domain"] = ",".join(sources)
        else:
            domains = NewsDomain.get_domains_for_country(country.value)
            if domains:
                params["domain"] = ",".join(domains)

        return params

    @staticmethod
    def _format_articles(raw_articles, delivery_method: str):
        """Extracts and formats only required fields from articles."""
        formatted_articles = []

        for article in raw_articles:
            extracted_article = {
                "title": article.get("title"),
                "keywords": article.get("keywords", []),
                "creator": article.get("creator", []),
                "source": article.get("source_id"),
                "description": article.get("description"),
                "content": article.get("content", "Content not available in free plan"),  # Handle missing content
                "pubDate": article.get("pubDate"),
                "language": article.get("language"),
                "category": article.get("category", []),
                "country": article.get("country", [])
            }

            # Apply delivery method transformation
            if delivery_method == "summary":
                extracted_article["content"] = extracted_article["description"]
            elif delivery_method == "bullet_points":
                extracted_article["content"] = "\n".join(f"- {point}" for point in extracted_article["keywords"][:5])
            elif delivery_method == "one_sentence":
                extracted_article["content"] = extracted_article["description"].split(".")[0] + "."

            formatted_articles.append(extracted_article)

        return formatted_articles

    @staticmethod
    def fetch_news_from_json(parsed_json: dict):
        """Processes the AI-extracted JSON and fetches relevant news."""
       #print(f"parsed json {parsed_json}")  # Debugging

        try:
            # Extract necessary parameters directly from parsed_json
            query = parsed_json.get("query")  # FIX: Extract query properly
            category = parsed_json.get("category")
            country = parsed_json.get("country")
            language = parsed_json.get("language")
            sources = parsed_json.get("sources")
            timeframe = parsed_json.get("timeframe")
            delivery_method = parsed_json.get("delivery_method", "default")  # Default to raw content

            # Properly validate and map category
            try:
                category_enum = Category[category.upper()] if category else None
            except KeyError:
                category_enum = None  # If invalid category, fallback to None

            # Properly validate and map country and language
            country_enum = Country(country) if country else Country.US
            language_enum = Language(language) if language else Language.ENGLISH

            # Properly prioritize sources over default domains
            if sources and isinstance(sources, list) and len(sources) > 0:
                domain_list = ",".join(sources)  # Use user-provided sources
            else:
                domain_list = ",".join(NewsDomain.get_domains_for_country(country_enum.value))

            # Prepare API request
            params = NewsService._get_api_params(
                query=query,
                category=category_enum,
                language=language_enum,
                country=country_enum,
                timeframe=timeframe,
                sources=sources
            )

            # Ensure domain is properly set
            params["domain"] = domain_list


            # Fetch news
            response = NewsService.api_client.news_api(**params)

            if response.get("status") == "error":
                return {
                    "error": response.get("results", {}).get("message", "Unknown error occurred"),
                    "error_code": ErrorCode.EXTERNAL_API_ERROR.value
                }

            # Format articles based on delivery method
            raw_articles = response.get("results", [])
            formatted_articles = NewsService._format_articles(raw_articles, delivery_method)
            #print(f"formated aritcales: {formatted_articles}")
            return formatted_articles

        except Exception as e:
            return {
                "error": f"Failed to fetch news: {str(e)}",
                "error_code": ErrorCode.EXTERNAL_API_ERROR.value
            }