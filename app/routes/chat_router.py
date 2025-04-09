from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.chatManager import ChatManager

router = APIRouter()
chat_manager = ChatManager()

class ChatRequest(BaseModel):
    userId: str | None = Field(None, title="User ID (optional)")
    requestBody: str = Field(..., title="User's query to NAO")

@router.post("/")
async def chat_with_nao(request: ChatRequest):
    """
    Processes user input:
    - Receives JSON input with userId (optional) and requestBody.
    - Sends it to the ChatManager.
    - Returns the structured AI response.
    """

    # Process the request through ChatManager
    response = await chat_manager.process_request(request.model_dump())

    # Check if an error occurred
    if "error_code" in response:
        return {"status": "error", "message": response["error"], "code": response["error_code"]}

    # Return the final AI response
    return {
        "status": "success",
        "response": response
    }
