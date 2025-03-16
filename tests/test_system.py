import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_system_health():
    """
    Tests if the FastAPI system starts correctly and responds.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "NAO Robot Backend is running"}

def test_chat_route_health():
    """
    Ensures the chat endpoint is reachable and returns a response.
    """
    response = client.get("/chat/?user_input=Hello")
    assert response.status_code == 200
    assert "command" in response.json() or "error" in response.json()  # Should return either valid output or error
