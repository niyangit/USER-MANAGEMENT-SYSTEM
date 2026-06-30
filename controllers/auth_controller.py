from fastapi import Depends, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from db.main import get_db_instance
from routes.auth_route import auth_router
from services.auth_service import AuthService
from schemas.user import LoginSchema
from utils.response import ApiResponse
from utils.auth import validate_jwt_token
from utils.jwt import create_access_token


from schemas.auth import (
    ForgotPasswordSchema,
    VerifyOtpSchema,
    ResetPasswordSchema
)
from utils.rate_limit import limiter


@auth_router.post("/login")
#@limiter.limit("5/minute")
def login(
    request: Request,
     
    login_data: LoginSchema,
    db: Session = Depends(get_db_instance)
):

    service = AuthService(db)

    result = service.login(login_data)

    return ApiResponse.success(
        data=result,
        message="Login successful"
    )

   

@auth_router.get("/me")
def get_current_logged_in_user(
    current_user=Depends(
        validate_jwt_token
    )
):

    return ApiResponse.success(
        data=current_user,
        message="Token is valid"
    )
@auth_router.post(
    "/forgot-password"
)
@limiter.limit(
    "3/minute"
)
def forgot_password(
    request: Request,
    forgot_request: ForgotPasswordSchema,

   
    db: Session = Depends(
        get_db_instance
    )
):

    service = AuthService(db)

    result = service.forgot_password(

        forgot_request.email,
        forgot_request.method
        
    )

    return ApiResponse.success(
        data=result,
        message="Email sent"
    )
@auth_router.post(
    "/reset-password"
)
@limiter.limit(
    "5/minute"
)
def reset_password(
    request: Request,

    reset_request:
    ResetPasswordSchema,

    

    db: Session =
    Depends(
        get_db_instance
    )
):

    service = AuthService(db)

    
    result = service.reset_password(
    reset_request.reset_token,
    reset_request.password
    
    )

    return ApiResponse.success(
        data=result,
        message=
        "Password reset successful"
    )

@auth_router.post(
    "/verify-otp"
)
@limiter.limit(
    "10/minute"
)
def verify_otp(
    request: Request,
    otp_request: VerifyOtpSchema,
    
    db: Session = Depends(
        get_db_instance
    )
):

    service = AuthService(db)

    result = service.verify_otp(
        otp_request.email,
        otp_request.otp
        
    )
   

    return ApiResponse.success(
        data=result,
        message="OTP verified"
    ) 




