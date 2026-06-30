from fastapi import Header

from jose import jwt, JWTError

from lib.execptions import UnauthorizedException

from utils.jwt import (
    SECRET_KEY,
    ALGORITHM
)


def validate_jwt_token(
    authorization: str = Header(None)
):

    if not authorization:

        raise UnauthorizedException(
            "JWT token required"
        )

    try:

        token = authorization.replace(
            "Bearer ",
            ""
        )

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        #print("JWT PAYLOAD:", payload)



        return payload

    except JWTError:

        raise UnauthorizedException(
            "Invalid JWT token"
        )