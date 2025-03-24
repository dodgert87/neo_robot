from app.services.query_generators.query_factory import QueryFactory
from app.core.enums import Tag, Country, Category, DeliveryMethod
from app.core.error_codes import ErrorCode
from app.core.language import Language


class QueryService:
    """
    Handles AI query generation and request processing.
    """

    @staticmethod
    def query_request(user_input: str) -> str:
        """
        Formats a structured request for AI to extract query details, including news parameters and language detection.
        """
        valid_tags = Tag.get_all_tags()  # Embed all valid tags in the prompt
        supported_languages = Language.get_all_languages()  # Get supported language codes
        valid_categories = [category.value for category in Category]
        valid_countries = [country.value for country in Country]
        valid_delivery_methods = [method.value for method in DeliveryMethod]

        return f"""
            Analyze the following user request and extract structured query details:

             **User Request**: "{user_input}"

            1️⃣ **Extracted Fields Explanation**:
            - `"command"`: The main action requested (e.g., "fetch news", "show latest news").
            - `"tag"`: The **category** of the request. Choose one from: **[{valid_tags}]**.
            - `"parameters"`: Extract relevant details **if available** (e.g., `location`, `time`, `category`, etc.).
            - `"confidence"`: Estimate **how confident** you are in understanding the request.
            - `"generalContext"`: Summarize **what the user is asking** in one sentence.
            - `"followUp"`: If this request is **a follow-up to a previous conversation**, include the relevant context.
            - `"emotion"`: Detect **user sentiment** (e.g., "happy", "curious", "frustrated") and assign a confidence score.
            - `"language"`: Detect the **language** of the request. Choose from: **[{supported_languages}]**.

            2️⃣ **Conditional Extraction for News Requests**:
            If `"tag"` is `"news"`, extract additional **news-specific parameters**:
            - `"query"`: The **specific topic or keyword** (e.g., `"Tesla"`, `"Bitcoin"`). Use `null` if not specified.
            - `"category"`: The **news category** (Choose from: **[{valid_categories}]**). Use `null` if not specified.
            - `"country"`: The **country for news** (Choose from: **[{valid_countries}]**). Use `null` if not specified.
            - `"language"`: The **language of news articles** (Choose from: **[{supported_languages}]**).
            - `"sources"`: A list of preferred news sources (if specified). Use `null` if not specified.
            - `"timeframe"`: The **timeframe** (e.g., `"6h"` for the last 6 hours, `"24h"` for 24 hours). Use `null` if not specified.
            - `"latest"`: If the user asked for **latest news**, this should be `true` or `false`.
            - `"delivery_method"`: Format for news response (Choose from: **[{valid_delivery_methods}]**). Default is `"default"`.

            3️⃣ **Return Format**:
            - **For News Requests**:
            {{
                "command": "fetch latest news",
                "tag": "news",
                "parameters": {{
                    "query": "Tesla",
                    "category": "business",
                    "country": "us",
                    "language": "en",
                    "sources": null,
                    "timeframe": "6h",
                    "latest": true,
                    "delivery_method": "summary"
                }},
                "confidence": {{
                    "level": 0.95,
                    "reason": "User explicitly asked for business news from the US in English."
                }},
                "generalContext": "User wants the latest business news from the US.",
                "followUp": {{
                    "status": false,
                    "context": null
                }},
                "emotion": {{
                    "type": "neutral",
                    "confidence": 0.7
                }},
                "language": "en"
            }}

            - **For Other Requests (Default Parsing)**:
            {{
                "command": "detected command",
                "tag": "detected tag from [{valid_tags}]",
                "parameters": {{ "param1": "value", "param2": "value" }},
                "confidence": {{ "level": 0.9, "reason": "explanation of confidence" }},
                "generalContext": "summary of the request",
                "followUp": {{ "status": false, "context": null }},
                "emotion": {{ "type": "neutral", "confidence": 0.0 }},
                "language": "detected language from [{supported_languages}]"
            }}

            ❗ **Unsupported Language Handling**:
            If the detected language is **not** in **[{supported_languages}]**, return:
            {{
                "error": "Unsupported language detected",
                "language": "detected language"
            }}

            🔹 **Ensure your response follows this JSON format exactly.**
            🔹 **Do not add extra explanations or comments.**
            🔹 **Use double quotes (`"`) for all string values.**
            """


    @staticmethod
    def generate_final_query(parsed_json: dict) -> dict:
        """
        Calls the correct Query Generator to format the AI query.
        """

        query_generator = QueryFactory.get_query_generator(parsed_json["tag"])

        if not query_generator:
            return {
                "error": "Unsupported query type.",
                "error_code": ErrorCode.UNKNOWN_QUERY.value
            }

        return query_generator.generate_query(parsed_json)