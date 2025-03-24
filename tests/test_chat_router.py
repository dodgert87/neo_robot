from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest

# Simulate the FastAPI app and the /chat endpoint
app = FastAPI()

@app.post("/chat/")
async def chat_with_nao(request: dict):
    user_input = request.get("requestBody", "")
    if not user_input:
        return {"status": "error", "message": "Invalid input", "code": 1000}
    if "joke" in user_input:
        return {"status": "error", "message": "AI failed to process request.", "code": 2001}
    return {
        "status": "success",
        "response": {
            "queryId": "test-query-id",
            "response": "Here's the weather in Paris..."
        }
    }

client = TestClient(app)

def test_chat_valid_request():
    response = client.post("/chat/", json={"requestBody": "Tell me the weather in Paris"})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert "response" in response_json
    assert "queryId" in response_json["response"]
    assert isinstance(response_json["response"]["response"], str)

def test_chat_empty_input():
    response = client.post("/chat/", json={"requestBody": ""})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "error"
    assert response_json["code"] == 1000
    assert "message" in response_json

def test_chat_ai_processing_error():
    response = client.post("/chat/", json={"requestBody": "Tell me a joke"})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "error"
    assert response_json["code"] == 2001
    assert "message" in response_json

def test_chat_response_contains_expected_fields():
    response = client.post("/chat/", json={"requestBody": "Tell me the weather in Paris"})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "success"
    assert "response" in response_json
    assert "queryId" in response_json["response"]
    assert "response" in response_json["response"]