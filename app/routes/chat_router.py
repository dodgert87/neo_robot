from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.request_service import RequestService

router = APIRouter()

class ChatRequest(BaseModel):
    userId: str | None = Field(None, title="User ID (optional)")
    requestBody: str = Field(..., title="User's query to NAO")

@router.post("/")
async def chat_with_nao(request: ChatRequest):
    """
    Processes user input:
    - Receives JSON input with userId (optional) and requestBody.
    - Sends it to the Request Service.
    - Returns the structured AI response.
    """

    # Process the request through RequestService (calls ResponseService internally)
    response = RequestService.process_request(request.model_dump())

    # Check if an error occurred
    if "error_code" in response:
        return {"status": "error", "message": response["error"], "code": response["error_code"]}

    # Return the final AI response (no extra AI call)
    return {
        "status": "success",
        "response": response
    }
