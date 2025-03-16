import pytest
import uuid
from app.services.request_service import RequestService
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
    response = RequestService.process_request("Tell me the weather in Paris")

    assert "error" not in response  # No errors should exist
    assert "queryId" in response  # Ensure unique query ID is assigned
    assert "response" in response  # AI response must exist
    assert isinstance(response["response"], str)  # Final response should be a string

def test_process_request_invalid(mock_uuid):
    """
    Tests invalid input handling.
    """
    response = RequestService.process_request("")

    assert "error" in response
    assert response["error_code"] == ErrorCode.INVALID_INPUT.value
    assert "queryId" in response  # Even errors should have a query ID

    response = RequestService.process_request("    ")  # Empty after cleaning
    assert "error" in response
    assert response["error_code"] == ErrorCode.AI_PROCESSING_ERROR.value
    assert "queryId" in response
