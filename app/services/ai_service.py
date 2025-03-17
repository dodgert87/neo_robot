import openai
from app.core.error_codes import ErrorCode
from app.core.config import settings


class AIService:
    """
    Handles AI model interactions.
    """

    client = None

    @staticmethod
    def initialize_client():
        if not AIService.client:
            OPENAI_API_KEY = settings.OPENAI_API_KEY
            if not OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found.")
            AIService.client = openai.Client(api_key=OPENAI_API_KEY)

    @staticmethod
    def call_ai_model(ai_query: str) -> str:
        """
        Calls the AI model with provided query.
        Returns raw string output without JSON parsing.
        """
        AIService.initialize_client()
        try:
            response = AIService.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": ai_query}],
            )
            ai_raw_response = response.choices[0].message.content.strip()
            return ai_raw_response

        except Exception as e:
            return f"AI request failed: {str(e)}"
