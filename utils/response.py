from datetime import datetime

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from sqlalchemy.exc import SQLAlchemyError


class ApiResponse:

    @staticmethod
    def success(
        data=None,
        message="Operation completed successfully",
        status_code=200
    ):
        return {
            "status": "success",
            "code": status_code,
            "message": message,
            "data": data,
            "meta": {
                "timestamp": datetime.utcnow().isoformat()
            }
        }

    @staticmethod
    def error(
        error_type,
        message,
        status_code,
        details=None
    ):
        return {
            "status": "error",
            "code": status_code,
            "error": {
                "type": error_type,
                "message": message,
                "details": details or []
            },
            "meta": {
                "timestamp": datetime.utcnow().isoformat()
            }
        }


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    details = []

    for error in exc.errors():

        details.append({
            "field": ".".join(
                map(str, error["loc"][1:])
            ),
            "issue": error["msg"]
        })

    return JSONResponse(
        status_code=400,
        content=ApiResponse.error(
            error_type="ValidationError",
            message="Invalid input provided",
            status_code=400,
            details=details
        )
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    error_type_map = {
        400: "BadRequest",
        401: "AuthenticationError",
        403: "AuthorizationError",
        404: "ResourceNotFound",
        409: "ConflictError",
        422: "BusinessRuleViolation",
        429: "RateLimitExceeded",
        500: "InternalServerError"
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse.error(
            error_type=error_type_map.get(
                exc.status_code,
                "HttpException"
            ),
            message=exc.detail,
            status_code=exc.status_code
        )
    )


async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError
):

    return JSONResponse(
        status_code=500,
        content=ApiResponse.error(
            error_type="DatabaseError",
            message="Database operation failed",
            status_code=500
        )
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content=ApiResponse.error(
            error_type="InternalServerError",
            message=str(exc),
            status_code=500
        )
    )