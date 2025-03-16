import openai
import os
from dotenv import load_dotenv
from app.core.error_codes import ErrorCode

# Load API key from environment
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path=dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_NAO_ROBOT")

class AIService:
    """
    Handles AI model interactions.
    """

    client = None

    @staticmethod
    def initialize_client():
        if not AIService.client:
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_NAO_ROBOT")
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
