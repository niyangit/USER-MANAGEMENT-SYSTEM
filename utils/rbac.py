from fastapi import Depends

from utils.auth import validate_jwt_token

from lib.execptions import (
    ForbiddenException
)


def require_role(
    role: str
):

    def checker(
        current_user=Depends(
            validate_jwt_token
        )
    ):

        if current_user["role"] != role:

            raise ForbiddenException(
                "Access denied"
            )

        return current_user

    return checker