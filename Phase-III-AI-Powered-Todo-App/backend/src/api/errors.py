from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict = {}


def handle_api_error(code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: dict = None):
    raise HTTPException(
        status_code=status_code,
        detail=ErrorResponse(code=code, message=message, details=details or {}).dict()
    )


class InvalidInputError(HTTPException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(code="INVALID_INPUT", message=message, details=details or {}).dict()
        )


class UnauthorizedError(HTTPException):
    def __init__(self, message: str = "Authentication required", details: dict = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(code="UNAUTHORIZED", message=message, details=details or {}).dict(),
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenError(HTTPException):
    def __init__(self, message: str = "Not authorized to perform this action", details: dict = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse(code="FORBIDDEN", message=message, details=details or {}).dict()
        )


class NotFoundError(HTTPException):
    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(code="NOT_FOUND", message=message, details=details or {}).dict()
        )
