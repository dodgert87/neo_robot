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

