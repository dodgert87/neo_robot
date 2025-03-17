from fastapi import APIRouter
from app.routes import chat_router
from app.routes import db_routes

# Create a main router
router = APIRouter()

# Include sub-routers
router.include_router(chat_router.router, prefix="/chat", tags=["Chat"])
router.include_router(db_routes.router, prefix="/db", tags=["db"])

