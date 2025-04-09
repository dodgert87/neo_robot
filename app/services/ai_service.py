import openai
import asyncio
from openai import OpenAI
from app.core.config import settings

class AIService:
    """
    Handles AI model interactions using OpenAI SDK v1+ with async-safe wrappers.
    """
    client: OpenAI = None

    @staticmethod
    def initialize_client():
        if not AIService.client:
            OPENAI_API_KEY = settings.OPENAI_API_KEY
            if not OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found.")
            AIService.client = OpenAI(api_key=OPENAI_API_KEY)

    @staticmethod
    async def call_ai_model(messages: list[dict[str, str]]) -> str:
        """
        Async-compatible wrapper for synchronous OpenAI client call.
        """
        AIService.initialize_client()

        def blocking_call():
            return AIService.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

        try:
            response = await asyncio.to_thread(blocking_call)
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI request failed: {str(e)}"
