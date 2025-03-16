from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.main_route import router as main_router
from app.core.config import settings
from app.core.middleware import RequestLoggingMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="NAO Robot Interaction Backend",
    description="Handles AI-driven interactions for NAO robot",
    version="1.0.0"
)

# Middleware for CORS (Allowing frontend access if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Include all API routes from main_route.py
app.include_router(main_router)

# Root route for health check
@app.get("/", tags=["System"])
def root():
    return {"message": "NAO Robot Backend is running"}
