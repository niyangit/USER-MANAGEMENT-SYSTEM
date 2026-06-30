from pydantic import BaseModel, EmailStr


class ForgotPasswordSchema(
    BaseModel
):
    email: EmailStr
    method: str


class VerifyOtpSchema(
    BaseModel
):
    email: EmailStr
    otp: str

class ResetPasswordSchema(
    BaseModel
):
    reset_token: str
    password: str