import uuid
from app.services.response_service import ResponseService
from app.core.error_codes import ErrorCode
from app.services.cache_service import CacheService

class RequestService:
    """
    Handles incoming requests: assigns unique query IDs, validates, cleans, and forwards to the response service.
    """

    @staticmethod
    def process_request(request_data: dict) -> dict:
        """
        Processes the user input:
        - Extracts `userId` (optional) and `requestBody` (string).
        - Assigns a unique query ID.
        - Checks if it's a follow-up query.
        - Cleans the text.
        - Sends it to ResponseService for AI processing.
        - Returns the structured JSON response.
        """

        user_id = request_data.get("userId")  # User ID (can be None)
        user_input = request_data.get("requestBody")  # User input text
        reference_query_id = None
        if not user_input or not isinstance(user_input, str) or user_input.strip() == "":
            return {
                "error": "Invalid input: No meaningful text found.",
                "error_code": ErrorCode.INVALID_INPUT.value,
                "queryId": str(uuid.uuid4()),  # Assign query ID for error tracking
            }

        query_id = str(uuid.uuid4())  # Generate unique query ID

       # Call ResponseService to process the request
        response = ResponseService.handle_request(user_input, query_id, reference_query_id)

        # Store the response in the database (including userId)
        CacheService.store_query(
            query_id=query_id,
            user_id=user_id,
            command=response.get("command"),
            tag=response.get("tag"),
            parameters=response.get("parameters", {}),
            response=response.get("response"),
            language_code=response.get("language_code", "en"),  # Default to English
        )

        return response
