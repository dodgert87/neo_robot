from app.services.query_generators.query_factory import QueryFactory
from app.core.enums import Tag
from app.core.error_codes import ErrorCode
from app.core.Language import Language


class QueryService:
    """
    Handles AI query generation and request processing.
    """

    @staticmethod
    def query_request(user_input: str) -> str:
        """
        Formats a structured request for AI to extract query details, including language detection.
        """
        valid_tags = Tag.get_all_tags()  # Embed all valid tags in the prompt
        supported_languages = Language.get_all_languages()  # Get supported language codes

        return f"""
        Analyze the following user request and extract structured query details:

        User Request: "{user_input}"

        1️⃣ **Extracted Fields Explanation**:
        - `"command"`: The main action requested.
        - `"tag"`: The **category** of the request. Choose one from: **[{valid_tags}]**.
        - `"parameters"`: Extract relevant details **if available** (e.g., `location`, `time`, `category`).
        - `"confidence"`: Estimate **how confident** you are in understanding the request.
        - `"generalContext"`: Summarize **what the user is asking** in one sentence.
        - `"followUp"`: If this request is **a follow-up to a previous conversation**, include the relevant context.
        - `"emotion"`: Detect **user sentiment** (e.g., "happy", "curious", "frustrated") and assign a confidence score.
        - `"language"`: Detect the **language** of the request. Choose from: **[{supported_languages}]**.

        2️⃣ **Return in JSON format**:
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

        ❗ If the detected language is **not** in **[{supported_languages}]**, return:
        {{
            "error": "Unsupported language detected",
            "language": "detected language"
        }}

        Your response must be in valid JSON format. Do not include any additional text, explanations, or code comments. Use double quotes, not single quotes.
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