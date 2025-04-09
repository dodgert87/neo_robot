import pytest
import uuid
from app.services.chatManager import RequestService
from app.core.error_codes import ErrorCode


@pytest.fixture
def mock_uuid(monkeypatch):
    """
    Mock UUID generation to ensure consistent test results.
    """
    monkeypatch.setattr(uuid, "uuid4", lambda: "test-uuid")

def test_process_request_valid(mock_uuid):
    """
    Tests valid input processing.
    """
    request_data = {
        "userId": "test-user",
        "requestBody": "Tell me the weather in Paris"
    }

    response = RequestService.process_request(request_data)

    assert "error" not in response  # No errors should exist
    assert "queryId" in response  # Ensure unique query ID is assigned
    assert "response" in response  # AI response must exist
    assert isinstance(response["response"], str)  # Final response should be a string


def test_process_request_invalid(mock_uuid):
    """
    Tests invalid input handling.
    """
    empty_input = {
        "userId": "test-user",
        "requestBody": ""
    }

    response = RequestService.process_request(empty_input)

    assert "error" in response
    assert response["error_code"] == ErrorCode.INVALID_INPUT.value
    assert "queryId" in response

    spaces_only = {
        "userId": "test-user",
        "requestBody": "   "
    }

    response = RequestService.process_request(spaces_only)
    assert "error" in response
    assert response["error_code"] == ErrorCode.INVALID_INPUT.value
    assert "queryId" in response
