from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(
            status_code=400,
            detail=detail
        )


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(
            status_code=401,
            detail=detail
        )


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(
            status_code=403,
            detail=detail
        )


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=404,
            detail=detail
        )


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            status_code=409,
            detail=detail
        )







class InternalServerException(HTTPException):
    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(
            status_code=500,
            detail=detail
        )
class AuthenticationException(
    HTTPException
):
    def __init__(
        self,
        message="Invalid credentials"
    ):
        super().__init__(
            status_code=401,
            detail=message
        )
class TooManyAttemptsException(
    HTTPException
):
    def __init__(
        self,
        detail="Too many failed login attempts. Try again in 1 minute."
    ):
        super().__init__(
            status_code=429,
            detail=detail
        )

