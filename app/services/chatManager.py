import uuid
from datetime import datetime
from typing import Dict, Optional

from app.core.error_codes import ErrorCode
from app.utils.string_utils import clean_text
from app.utils.id_utils import generate_chat_id, generate_fallback_user_id
from app.services.chatSession import ChatSession

class ChatManager:
    """
    Manages active chat sessions and routes user input to the appropriate ChatSession.
    """

    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}

    def process_request(self, request_data: dict) -> dict:
        """
        Processes the user input:
        - Extracts `userId` (optional) and `requestBody` (string).
        - Cleans the text.
        - Routes to an existing or new ChatSession instance.
        - Returns the structured JSON response.
        """
        user_id = request_data.get("userId")
        user_input = request_data.get("requestBody")

        if not user_input or not isinstance(user_input, str) or user_input.strip() == "":
            return {
                "error": "Invalid input: No meaningful text found.",
                "error_code": ErrorCode.INVALID_INPUT.value,
                "queryId": str(uuid.uuid4()),  # Error tracking only
            }

        cleaned_input = clean_text(user_input)

        # Handle missing user ID
        if not user_id:
            user_id = generate_fallback_user_id()

        chat_id = generate_chat_id(user_id)

        # Get or create a ChatSession
        session = self.get_or_create_session(chat_id)

        # Process input in the session (async in future if needed)
        return session.handle_input(cleaned_input)

    def get_or_create_session(self, chat_id: str) -> ChatSession:
        if chat_id not in self.sessions:
            self.sessions[chat_id] = ChatSession(chat_id)
        return self.sessions[chat_id]

    def delete_session(self, chat_id: str) -> None:
        if chat_id in self.sessions:
            del self.sessions[chat_id]

    def load_session(self, chat_id: str) -> Optional[ChatSession]:
        return self.sessions.get(chat_id)

    def get_all_sessions(self) -> Dict[str, ChatSession]:
        return self.sessions
