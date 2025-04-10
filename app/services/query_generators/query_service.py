from app.services.query_generators.query_factory import QueryFactory
from app.core.enums import Tag, Country, Category, DeliveryMethod
from app.core.error_codes import ErrorCode
from app.core.language import Language


class QueryService:
    """
    Handles AI query generation and request processing.
    """

    @staticmethod
    def query_request(user_input: str) -> dict:
        """
        Formats a message object to send to the AI for extracting query details.
        Returns:
            dict: {"role": "user", "content": <formatted prompt>}
        """
        return {
            "role": "user",
            "content": QueryService.build_prompt(user_input)
        }

    @staticmethod
    def build_prompt(user_input: str) -> str:
        """
        Builds the full prompt text for the AI model based on the user's input.
        """
        valid_tags = Tag.get_all_tags()
        supported_languages = Language.get_all_languages()
        valid_categories = [category.value for category in Category]
        valid_countries = [country.value for country in Country]
        valid_delivery_methods = [method.value for method in DeliveryMethod]

        return f"""
        Analyze the following user request and extract structured query details:

        **User Request**: "{user_input}"

        1️⃣ **Extracted Fields Explanation**:
        - "command": The main action requested (e.g., "fetch news", "check weather", "summarize update").
        - "tag": The main category of the request. Choose one from: [{valid_tags}].
        - "parameters": Extract relevant details if available (e.g., "location", "date", "topic", etc.).
        - "requires_fetch": true or false — whether the assistant needs to fetch new external information from these type of topics [{valid_tags}].
        - "follow_up": true if the request indicates that it continues from a previous interaction.
        - "context": An object describing any contextual dependencies required to fulfill the request.
        - "requires_context": true or false
        - "context_type": The domain of the context (must match one of: [{valid_tags}])
        - "context_parameters": Extract relevant inputs from the user request or infer from previous turns. Use the parameter rules below for matching tags.
        - "confidence": An object with "level" (float from 0.0 to 1.0) and a short "reason".
        - "generalContext": Summary of the user’s request in one sentence.
        - "emotion": An object with "type" (e.g., "curious", "frustrated") and a "confidence" score.
        - "language": Language of the request (must be one of: [{supported_languages}])

        2️⃣ **Conditional Parameter Extraction**:
        - For tag = "news" or context_type = "news", extract:
        - "query": Specific topic or keyword
        - "category": One of [{valid_categories}]
        - "country": One of [{valid_countries}]
        - "language": One of [{supported_languages}]
        - "sources": List of sources if specified
        - "timeframe": (e.g., "6h", "24h")
        - "latest": true or false
        - "delivery_method": One of [{valid_delivery_methods}]

        - For tag = "weather" or context_type = "weather", extract:
        - "location": (e.g., "Helsinki")
        - "date": (e.g., "today", "tomorrow")

        3️⃣ **Example Return Format**:
        {{
        "command": "check ski suitability in the alps today",
        "tag": "general",
        "parameters": {{
            "activity": "skiing",
            "location": "Alps",
            "date": "today"
        }},
        "requires_fetch": true,
        "follow_up": false,
        "context": {{
            "requires_context": true,
            "context_type": "weather",
            "context_parameters": {{
            "location": "Alps",
            "date": "today"
            }}
        }},
        "confidence": {{
            "level": 0.91,
            "reason": "User asked about skiing today in the Alps, which requires current weather."
        }},
        "generalContext": "Check if skiing is possible today in the Alps.",
        "emotion": {{
            "type": "curious",
            "confidence": 0.7
        }},
        "language": "en"
        }}

        ❗ **Unsupported Language Handling**:
        If the detected language is not in [{supported_languages}], return:
        {{
        "error": "Unsupported language detected",
        "language": "detected language"
        }}

        🔹 Ensure your response follows this JSON format exactly.
        🔹 Do not add extra explanations or comments.
        🔹 Use double quotes (\"\") for all string values.
        """.strip()



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
