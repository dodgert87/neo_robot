from fastapi import APIRouter, Query
from app.services.request_service import RequestService

router = APIRouter()

@router.get("/")
async def chat_with_nao(user_input: str = Query(..., title="User's query to NAO")):
    """
    Processes user input:
    - Cleans the request.
    - Sends it to the Request Service (which calls Response Service internally).
    - Returns the structured AI response.
    """

    # Process the request through RequestService (calls ResponseService internally)
    response = RequestService.process_request(user_input)

    # Check if an error occurred
    if "error_code" in response:
        return {"status": "error", "message": response["error"], "code": response["error_code"]}

    # Return the final AI response (no extra AI call)
    return {
        "status": "success",
        "response": response
    }
