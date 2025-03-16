import uuid
from app.services.response_service import ResponseService

class RequestService:
    """
    Handles incoming requests: assigns unique query IDs, validates, cleans, and forwards to the response service.
    """

    @staticmethod
    def process_request(user_input: str, reference_query_id: str = None) -> dict:
        """
        Processes the user input:
        - Assigns a unique query ID.
        - Checks if it's a follow-up query.
        - Cleans the text.
        - Sends it to ResponseService for AI processing.
        - Returns the structured JSON response.
        """

        query_id = str(uuid.uuid4())  # Generate unique query ID

        # Send request to ResponseService
        return ResponseService.handle_request(user_input, query_id, reference_query_id)
