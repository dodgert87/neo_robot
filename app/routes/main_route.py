from fastapi import APIRouter, Query, HTTPException
from app.routes import chat_router
from app.routes import db_routes
from app.models.api_models import NewsRequest
from app.services.news_service import NewsService


# Create a main router
router = APIRouter()

# Include sub-routers
router.include_router(chat_router.router, prefix="/chat", tags=["Chat"])
router.include_router(db_routes.router, prefix="/db", tags=["db"])

@router.post("/news/fetch")
async def fetch_news(request: NewsRequest):
    """
    Fetches news dynamically based on the request parameters.
    - Accepts `query`, `category`, `language`, `country`, `timeframe`, `sources`, and `delivery_method`.
    - Returns formatted news articles.
    """
    try:
        # Call the news service with the provided JSON payload
        #print(f"the request from jason {request.model_dump()}")
        news = NewsService.fetch_news_from_json(request.model_dump())

        # Check if there's an error
        if "error" in news:
            raise HTTPException(status_code=400, detail=news["error"])

        return {"status": "success", "articles": news}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")