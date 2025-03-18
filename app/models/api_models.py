from pydantic import BaseModel
from typing import Optional

class PersonRequest(BaseModel):
    personId: str
    firstName: str
    lastName: str


class NewsArticleRequest(BaseModel):
    articleId: str
    queryId: Optional[str] = None
    title: str
    keywords: list[str]
    creator: Optional[list[str]] = None
    description: Optional[str] = None
    content: Optional[str] = None
    pubDate: str
    language: str
    category: list[str]
    country: list[str]
    sourceId: str
    sourceName: str
    sourceUrl: str
    imageUrl: Optional[str] = None


class NewsRequest(BaseModel):
    """Request model for fetching news dynamically."""
    query: str | None = None
    category: str | None = None
    language: str = "en"
    country: str = "us"
    timeframe: str | None = None
    sources: list[str] | None = None
    delivery_method: str = "default"
