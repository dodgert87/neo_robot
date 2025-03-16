import pytest
import requests
from unittest.mock import patch
from app.services.weather_service import WeatherService
from app.core.error_codes import ErrorCode


@pytest.fixture
def mock_weather_api_response():
    """
        Returns a sample successful weather API response.
    """
    return {
        "location": {
            "name": "Paris",
            "region": "Ile-de-France",
            "country": "France"
        },
        "current": {
            "last_updated": "2025-03-16 14:00",
            "temp_c": 12.5,
            "condition": {"text": "Cloudy"},
            "humidity": 55,
            "wind_kph": 10.2,
            "feelslike_c": 11.0,
            "cloud": 80
        }
    }


@patch("requests.get")
def test_get_weather_success(mock_get, mock_weather_api_response):
    """
        Tests successful weather data retrieval.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_weather_api_response

    response = WeatherService.get_weather("Paris")

    assert "error" not in response
    assert response["location"] == "Paris"
    assert response["region"] == "Ile-de-France"
    assert response["country"] == "France"
    assert response["weather"]["temperature_c"] == 12.5
    assert response["weather"]["condition"] == "Cloudy"
    assert response["weather"]["humidity"] == 55


@patch("requests.get")
def test_get_weather_invalid_location(mock_get):
    """
        Tests handling of an invalid location.
    """
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {"error": {"message": "No matching location found"}}

    response = WeatherService.get_weather("InvalidCity")

    assert "error" in response
    assert response["error_code"] == ErrorCode.INTERNAL_ERROR.value


@patch("requests.get")
def test_get_weather_api_failure(mock_get):
    """
        Tests API failure (simulating network error or API downtime).
    """
    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    response = WeatherService.get_weather("Paris")

    assert "error" in response
    assert "Failed to fetch weather" in response["error"]
    assert response["error_code"] == ErrorCode.INTERNAL_ERROR.value


def test_get_weather_missing_api_key(monkeypatch):
    """
        Tests missing API key scenario.
    """
    monkeypatch.setattr("app.services.weather_service.WEATHER_API_KEY", None)

    response = WeatherService.get_weather("Paris")

    assert "error" in response
    assert response["error"] == "Weather API key is missing."
    assert response["error_code"] == ErrorCode.INTERNAL_ERROR.value
