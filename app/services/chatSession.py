from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import uuid

from app.services.query_generators.query_service import QueryService
from app.services.ai_service import AIService
from app.core.language import Language
from app.core.error_codes import ErrorCode
from app.utils.json_utils import clean_and_parse_json
from app.utils.string_utils import clean_text

DEFAULT_SYSTEM_PROMPT = """
You are a helpful assistant to an elderly person who is asking questions, making your answer friendly and straightforward.
""".strip()

DEFAULT_PARSE_PROMPT = """
You are an analysis machine and your job is to extract relevant information according to a given requirement.
""".strip()

class ChatSession:
    """
    Represents a stateful chat session for a specific user.
    Handles input processing, maintains history, and interacts with the AI.
    """

    def __init__(self, chat_id: str, user_id: Optional[str] = None):
        self.chat_id = chat_id
        self.user_id = user_id
        self.language: Optional[Language] = None
        self.system_prompt: str = DEFAULT_SYSTEM_PROMPT
        self.parse_prompt: str = DEFAULT_PARSE_PROMPT
        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt, "timestamp": datetime.now(timezone.utc).isoformat()}
        ]

    async def handle_input(self, user_input: str) -> dict:
        cleaned_input = clean_text(user_input)
        query_id = str(uuid.uuid4())

        # Step 1: Generate AI extraction message
        ai_extraction_message = QueryService.query_request(cleaned_input)

        # Step 2: Call AI model with dynamic parse prompt + user message
        extraction_messages = [
            {"role": "system", "content": self.parse_prompt},
            ai_extraction_message
        ]
        print(f"extraction message is {extraction_messages}")
        ai_raw_response = await AIService.call_ai_model(messages=extraction_messages)
        print(f"ai raw response  is {ai_raw_response}")

        # Step 3: Parse JSON
        extracted_json = clean_and_parse_json(ai_raw_response)
        print(f"extracted jason is {extracted_json}")

        # Step 4: Error handling
        if "error" in extracted_json:
            if extracted_json["error"] == "Unsupported language detected":
                return {
                    "queryId": query_id,
                    "error": "Unsupported language detected",
                    "language": extracted_json.get("language"),
                    "error_code": ErrorCode.UNSUPPORTED_LANGUAGE.value
                }
            return {
                "queryId": query_id,
                "error": "AI failed to extract query details.",
                "error_code": ErrorCode.AI_PROCESSING_ERROR.value
            }

        # Track language in session
        self.language = Language(extracted_json["language"])

        # Step 5: Generate the final query
        extracted_json["queryId"] = query_id
        ai_query = QueryService.generate_final_query(extracted_json)

        if "error" in ai_query:
            return {
                "queryId": query_id,
                "error": ai_query["error"],
                "error_code": ai_query["error_code"]
            }

        # Step 6: Final AI call with system prompt and full chat context
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + [
            {"role": m["role"], "content": m["content"]} for m in self.history[1:]
        ] + [
            {"role": "user", "content": ai_query}
        ]

        ai_response = await AIService.call_ai_model(messages=messages)

        if "error" in ai_response:
            return {
                "queryId": query_id,
                "error": ai_response,
                "error_code": ErrorCode.AI_PROCESSING_ERROR.value
            }

        final_response = clean_text(ai_response)

        # Step 7: Update history
        now = datetime.now(timezone.utc).isoformat()
        self.history.append({"role": "user", "content": user_input, "timestamp": now})
        self.history.append({"role": "assistant", "content": final_response, "timestamp": now})

        # Step 8: Return structured response
        return {
            "queryId": query_id,
            "command": extracted_json["command"],
            "tag": extracted_json["tag"],
            "parsed_command": {
                "command": extracted_json["command"],
                "parameters": extracted_json["parameters"]
            },
            "raw_command": user_input,
            "response": final_response,
            "language_code": extracted_json["language"],
            "source": "AI"
        }

    def set_system_prompt(self, prompt: str) -> None:
        self.system_prompt = prompt
        self.history[0] = {
            "role": "system",
            "content": self.system_prompt,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def get_system_prompt(self) -> str:
        return self.system_prompt

    def set_parse_prompt(self, prompt: str) -> None:
        self.parse_prompt = prompt

    def get_parse_prompt(self) -> str:
        return self.parse_prompt
