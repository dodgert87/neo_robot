import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.error_codes import ErrorCode

client = TestClient(app)

def test_chat_valid_request():
    """
        Tests a valid user input to ensure a successful response.
    """
    response = client.get("/chat/?user_input=Tell me the weather in Paris")

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["status"] == "success"
    assert "response" in response_json
    assert "queryId" in response_json["response"]  # Ensures the response has a query ID
    assert isinstance(response_json["response"]["response"], str)  # AI response should be a string


def test_chat_empty_input():
    """
        Tests if the chat route properly handles an empty input.
    """
    response = client.get("/chat/?user_input=")

    assert response.status_code == 200  # API still returns 200, but with an error inside
    response_json = response.json()

    assert response_json["status"] == "error"
    assert response_json["code"] == ErrorCode.INVALID_INPUT.value  # Should return INVALID_INPUT error
    assert "message" in response_json  # Error message should exist


def test_chat_ai_processing_error(monkeypatch):
    """
        Simulates an AI failure during processing and checks for proper error handling.
    """

    def mock_process_request(*args, **kwargs):
        return {
            "error": "AI failed to process request.",
            "error_code": ErrorCode.AI_PROCESSING_ERROR.value
        }

    # Mock the function to simulate an AI failure
    monkeypatch.setattr("app.services.request_service.RequestService.process_request", mock_process_request)

    response = client.get("/chat/?user_input=Tell me a joke")
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["status"] == "error"
    assert response_json["code"] == ErrorCode.AI_PROCESSING_ERROR.value  # Expect AI error
    assert "message" in response_json  # Error message should exist


def test_chat_response_contains_expected_fields():
    """
        Ensures the response contains all expected fields when processing is successful.
    """
    response = client.get("/chat/?user_input=Tell me the weather in Paris")

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["status"] == "success"
    assert "response" in response_json
    assert "queryId" in response_json["response"]
    assert "response" in response_json["response"]
