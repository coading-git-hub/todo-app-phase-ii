from fastapi import Request, Response
from fastapi.responses import StreamingResponse
import logging
import time
import json
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request
        start_time = time.time()

        # Get request details
        request_details = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client": request.client.host if request.client else None,
        }

        # Skip logging sensitive data like authorization headers
        if "authorization" in request_details["headers"]:
            request_details["headers"]["authorization"] = "***"
        if "Authorization" in request_details["headers"]:
            request_details["headers"]["Authorization"] = "***"

        logger.info(f"Request: {json.dumps(request_details, default=str)}")

        # Process the request
        response: Response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        response_details = {
            "status_code": response.status_code,
            "process_time": f"{process_time:.4f}s",
            "content_length": response.headers.get("content-length", "unknown"),
        }

        logger.info(f"Response: {json.dumps(response_details)}")

        return response