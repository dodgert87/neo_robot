from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.main_route import router as main_router
from app.core.middleware import RequestLoggingMiddleware
from app.database.database import init_db
from contextlib import contextmanager

# Initialize FastAPI app
app = FastAPI(
    title="NAO Robot Interaction Backend",
    description="Handles AI-driven interactions for NAO robot",
    version="1.0.0"
)

# Middleware for CORS (Allowing frontend access if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://128.214.252.141:90",
    "http://128.214.252.141:8090",
    # Add more dev origins if needed
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Include all API routes from main_route.py
app.include_router(main_router)

# Initlazing database
init_db()

# Root route for health check
@app.get("/", tags=["System"])
def root():
    return {"message": "NAO Robot Backend is running"}
