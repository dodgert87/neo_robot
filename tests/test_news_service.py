import pytest
from unittest.mock import patch
from app.services.news_service import NewsService
from app.core.enums import Category, Country
from app.core.language import Language
from app.core.news_domain import NewsDomain

# Sample response for mock API calls
MOCK_API_RESPONSE = {
    "status": "success",
    "results": [
        {
            "title": "AI Advances in 2025",
            "keywords": ["AI", "technology"],
            "creator": ["John Doe"],
            "source_id": "cnn",
            "description": "Breakthroughs in AI are changing the tech landscape.",
            "content": "ONLY AVAILABLE IN PAID PLANS",
            "pubDate": "2025-03-18 14:00:00",
            "language": "en",
            "category": ["technology"],
            "country": ["us"]
        }
    ]
}

@pytest.fixture
def sample_json():
    """Sample parsed JSON for news fetching."""
    return {
        "query": "AI technology",
        "category": "technology",
        "language": "en",
        "country": "us",
        "timeframe": None,
        "sources": ["cnn", "bbc"],
        "delivery_method": "default"
    }

### ---- Test `_get_api_params` ---- ###
def test_get_api_params():
    """Test if API parameters are generated correctly."""
    params = NewsService._get_api_params(
        query="AI",
        category=Category.TECHNOLOGY,
        language=Language.ENGLISH,
        country=Country.US,
        timeframe="6h",
        sources=["cnn", "bbc"]
    )

    assert params["q"] == "AI"
    assert params["category"] == "technology"
    assert params["language"] == "en"
    assert params["country"] == "us"
    assert params["timeframe"] == "6h"
    assert params["domain"] == "cnn,bbc"

### ---- Test `_format_articles` ---- ###
def test_format_articles():
    """Test formatting of articles."""
    raw_articles = MOCK_API_RESPONSE["results"]
    formatted_articles = NewsService._format_articles(raw_articles, "default")

    assert len(formatted_articles) == 1
    assert formatted_articles[0]["title"] == "AI Advances in 2025"
    assert formatted_articles[0]["description"] == "Breakthroughs in AI are changing the tech landscape."
    assert formatted_articles[0]["language"] == "en"

def test_format_articles_summary():
    """Test summary delivery method."""
    raw_articles = MOCK_API_RESPONSE["results"]
    formatted_articles = NewsService._format_articles(raw_articles, "summary")

    assert formatted_articles[0]["content"] == formatted_articles[0]["description"]

def test_format_articles_bullet_points():
    """Test bullet points delivery method."""
    raw_articles = MOCK_API_RESPONSE["results"]
    formatted_articles = NewsService._format_articles(raw_articles, "bullet_points")

    assert formatted_articles[0]["content"].startswith("- AI")

def test_format_articles_one_sentence():
    """Test one sentence delivery method."""
    raw_articles = MOCK_API_RESPONSE["results"]
    formatted_articles = NewsService._format_articles(raw_articles, "one_sentence")

    assert formatted_articles[0]["content"].endswith(".")

### ---- Test `fetch_news_from_json` with mock API response ---- ###
@patch.object(NewsService.api_client, 'news_api', return_value=MOCK_API_RESPONSE)
def test_fetch_news_from_json(mock_api, sample_json):
    """Test news fetching from AI JSON with mock API response."""
    articles = NewsService.fetch_news_from_json(sample_json)

    assert len(articles) == 1
    assert articles[0]["title"] == "AI Advances in 2025"
    assert articles[0]["source"] == "cnn"
    assert mock_api.called

### ---- Test `fetch_news_from_json` with error handling ---- ###
@patch.object(NewsService.api_client, 'news_api', return_value={"status": "error", "results": {"message": "Invalid query"}})
def test_fetch_news_from_json_error(mock_api, sample_json):
    """Test error handling when API returns an error."""
    response = NewsService.fetch_news_from_json(sample_json)

    assert "error" in response
    assert response["error_code"] == 3001
    assert mock_api.called

### ---- Test `fetch_news_from_json` with no results ---- ###
@patch.object(NewsService.api_client, 'news_api', return_value={"status": "success", "results": []})
def test_fetch_news_from_json_no_results(mock_api, sample_json):
    """Test handling when API returns no results."""
    articles = NewsService.fetch_news_from_json(sample_json)

    assert articles == []
    assert mock_api.called
