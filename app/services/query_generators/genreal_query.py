from app.services.query_generators.base_query import BaseQueryGenerator

class GeneralQueryGenerator(BaseQueryGenerator):
    """
    Generates a natural AI prompt for general or unstructured user questions.
    """

    def generate_query(self, parsed_json: dict) -> str:
        """
        Formats a natural language prompt using the original user command, context, emotion, and language.
        """
        command = parsed_json.get("command", "unknown request")
        context = parsed_json.get("generalContext", "")
        emotion = parsed_json.get("emotion", {}).get("type", "neutral")
        language = parsed_json.get("language", "en")  # default to English

        return (
            f"You are a helpful assistant. The user asked the following question in language '{language}':\n\n"
            f"\"{command}\"\n\n"
            f"Context: {context or 'None provided'}\n"
            f"User sentiment: {emotion}\n\n"
            f"Please reply in the same language ({language}) using a tone appropriate to the emotion. "
            f"Be natural, clear, and helpful. Keep it concise, but informative."
        )
