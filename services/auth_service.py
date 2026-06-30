from sqlalchemy.orm import Session

from models.User import User
from utils.bcrypt import bcrypt
from utils.jwt import create_access_token

from lib.execptions import (
    NotFoundException,
    AuthenticationException ,
    TooManyAttemptsException
)

import schemas.user 

import random

from datetime import (
    datetime,
    timedelta
)

'''from utils.email import (
    send_email
)'''

from utils.email1 import send_email

from jose import jwt

from utils.jwt import (
    SECRET_KEY,
    ALGORITHM
)
from utils.login_attempts import failed_logins





class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def login(
        self,
        login_data: schemas.user.LoginSchema

    ):

        user = self.db.query(User).filter(
            User.email == login_data.email
        ).first()

        if not user:
            raise NotFoundException(
                f"User with email '{login_data.email}' not found"
            )
        if not user.is_active:

            raise AuthenticationException(
        "Account is blocked"
    )
        attempts = failed_logins.get(
    login_data.email,
    0
)

        if attempts >= 5:
            raise TooManyAttemptsException()
            
            

    

        if not bcrypt.verify(
            login_data.password,
            user.password
        ):
            failed_logins[
                login_data.email
            ]= attempts + 1

      
            raise AuthenticationException(
                "Invalid password"
            )
        access_token = create_access_token(
            {
                "user_id": user.id,
                "email": user.email,
                "role": user.role

            }
        )
        failed_logins.pop(
            login_data.email,
            None
        )

    
    

        
        '''print({
    "user_id": user.id,
    "email": user.email,
    "role": user.role
})'''

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    def forgot_password(
        self,
        email: str,
        method: str
    ):

        user = self.db.query(
            User
        ).filter(
            User.email == email
        ).first()

        if not user:

            raise NotFoundException(
                "User not found"
            )

        if method == "otp":

            otp = str(
                random.randint(
                    100000,
                    999999
                )
            )

            user.otp = otp

            user.otp_expiry = (
                datetime.utcnow()
                + timedelta(
                    minutes=5
                )
            )

            self.db.commit()

            send_email(
                user.email,
                "Password Reset OTP",
                f"""
Your OTP is:

{otp}

Valid for 5 minutes.
"""
            )

            return {
                "message":
                "OTP sent successfully"
            }

        if method == "link":

            token = create_access_token(
                {
                    "email": user.email,
                    "purpose": "reset_password"
                }
            )

            user.reset_token = token

            user.reset_token_expiry = (
                datetime.utcnow()
                + timedelta(
                    minutes=15
                )
            )

            self.db.commit()

            link = (
                "https://user-management-system-36zz.onrender.com"
                "/frontend/pages/reset_password.html"
                f"?token={token}"
            )

            send_email(
                user.email,
                "Reset Password Link",
                f"""
Click below link:

{link}

Valid for 15 minutes.
"""
            )

            return {
                "message":
                "Reset link sent successfully"
            }

        raise ValueError(
            "Invalid method"
        )
    def verify_otp(
        self,
        email: str,
        otp: str
    ):

        user = self.db.query(
            User
        ).filter(
            User.email == email
        ).first()

        if not user:

            raise NotFoundException(
                "User not found"
            )

        if user.otp != otp:

            raise AuthenticationException(
                "Invalid OTP"
            )

        if (
            datetime.utcnow()
            > user.otp_expiry
        ):

            raise AuthenticationException(
                "OTP expired"
            )

        reset_token = create_access_token(
            {
                "email": user.email,
                "purpose": "reset_password"
            }
        )

        user.reset_token = reset_token

        user.reset_token_expiry = (
            datetime.utcnow()
            + timedelta(
                minutes=15
            )
        )

        self.db.commit()

        return {
            "reset_token":
            reset_token
        }
    def reset_password(
        self,
        reset_token: str,
        password: str
    ):

        user = self.db.query(
            User
        ).filter(
            User.reset_token == reset_token
        ).first()

        if not user:

            raise AuthenticationException(
                "Invalid reset token"
            )

        if (
            datetime.utcnow()
            >
            user.reset_token_expiry
        ):

            raise AuthenticationException(
                "Reset token expired"
            )

        payload = jwt.decode(
            reset_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload["purpose"] != "reset_password":

            raise AuthenticationException(
                "Invalid token"
            )

        user.password = bcrypt.hash(
            password
        )

        user.otp = None
        user.otp_expiry = None

        user.reset_token = None
        user.reset_token_expiry = None

        self.db.commit()

        return {
            "message":
            "Password reset successful"
        }