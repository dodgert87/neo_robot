import pytest
import uuid
from app.services.response_service import ResponseService
from app.services.ai_service import AIService
from app.services.query_generators.query_service import QueryService
from app.utils.json_utils import clean_and_parse_json
from app.core.error_codes import ErrorCode

@pytest.fixture
def mock_uuid():
    """
    Generates a consistent mock UUID for testing.
    """
    return str(uuid.uuid4())


@pytest.fixture
def mock_ai_extraction_response(monkeypatch):
    """
    Mocks AI extraction response.
    """
    def mock_call_ai_model_extraction(*args, **kwargs):
        return '''{
            "command": "get_news",
            "tag": "news",
            "parameters": {"category": "latest"},
            "confidence": {"level": 0.9, "reason": "Detected news-related query."},
            "generalContext": "User is asking for news.",
            "followUp": {"status": true, "referenceQueryId": "test-followup-id"},
            "emotion": {"type": "neutral", "confidence": 0.0}
        }'''

    monkeypatch.setattr(AIService, "call_ai_model", mock_call_ai_model_extraction)


@pytest.fixture
def mock_ai_response_generation(monkeypatch):
    """
    Mocks AI response generation.
    """

    def mock_call_ai_model_response(*args, **kwargs):
        return "Here are the latest news headlines for today."

    monkeypatch.setattr(AIService, "call_ai_model", mock_call_ai_model_response)



def test_handle_request_ai_extraction_failure(monkeypatch, mock_uuid):
    """
        Simulates an AI failure during query extraction.
    """

    def mock_call_ai_model_extraction_fail(*args, **kwargs):
        return '{"error": "AI extraction failed"}'

    monkeypatch.setattr(AIService, "call_ai_model", mock_call_ai_model_extraction_fail)

    response = ResponseService.handle_request("Tell me the latest news", query_id=mock_uuid)

    assert response["queryId"] == mock_uuid
    assert response["error"] == "AI failed to extract query details."
    assert response["error_code"] == ErrorCode.AI_PROCESSING_ERROR.value


def test_handle_request_ai_response_failure(monkeypatch, mock_uuid, mock_ai_extraction_response):
    """
        Simulates an AI failure during response generation.
    """

    def mock_call_ai_model_response_fail(*args, **kwargs):
        return '{"error": "AI response failed"}'

    monkeypatch.setattr(AIService, "call_ai_model", mock_call_ai_model_response_fail)

    response = ResponseService.handle_request("Tell me the latest news", query_id=mock_uuid)

    assert response["queryId"] == mock_uuid
    assert "error" in response
    assert response["error_code"] == ErrorCode.AI_PROCESSING_ERROR.value

"""
def test_handle_request_followup(mock_uuid, mock_ai_extraction_response, mock_ai_response_generation):

        Tests handling a follow-up query.

    reference_query_id = str(uuid.uuid4())  # Simulate an existing query ID
    response = ResponseService.handle_request("Tell me more about it", query_id=mock_uuid, reference_query_id=reference_query_id)

    assert "queryId" in response
    assert response["queryId"] == mock_uuid
    assert response["followUp"]["referenceQueryId"] == reference_query_id
"""