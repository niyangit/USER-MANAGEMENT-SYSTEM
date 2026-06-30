import re

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator
)


class NewUserSchema(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=20
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError(
                "Name cannot be empty"
            )

        # Allow:
        # lowercase
        # uppercase
        # digits
        # special chars
        # spaces

        if not re.fullmatch(
            r"[A-Za-z0-9\s!@#$%^&*()_+\-=\[\]{};:'\",.<>/?\\|`~]+",
            value
        ):
            raise ValueError(
                "Name contains invalid characters"
            )

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain at least one digit"
            )

        if not re.search(
            r"[!@#$%^&*()_+\-=\[\]{};:'\",.<>/?\\|`~]",
            value
        ):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return value


class UserResponse(BaseModel):

    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True
class LoginSchema(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=20
    )