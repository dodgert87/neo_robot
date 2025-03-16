from fastapi import APIRouter
from app.routes import chat_router, news_router, weather_router
# Create a main router
router = APIRouter()

# Include sub-routers
router.include_router(chat_router.router, prefix="/chat", tags=["Chat"])
#router.include_router(news_router.router, prefix="/news", tags=["News"])
#router.include_router(weather_router.router, prefix="/weather", tags=["Weather"])
