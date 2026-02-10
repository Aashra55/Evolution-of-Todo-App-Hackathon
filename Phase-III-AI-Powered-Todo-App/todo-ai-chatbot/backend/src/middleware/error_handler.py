# backend/src/middleware/error_handler.py
import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:
            logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        except Exception as exc:
            logger.exception(f"Unhandled error during request to {request.url}: {exc}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"},
            )
