from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger("uvicorn")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url} - {response.status_code} ({process_time:.2f}s)")
        return response
