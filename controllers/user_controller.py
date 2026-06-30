from fastapi import Depends
from sqlalchemy.orm import Session

from routes.user_route import user_router

from schemas.user import NewUserSchema

from db.main import get_db_instance

from services.user_service import UserService

from utils.response import ApiResponse

from utils.auth import validate_jwt_token
from utils.rbac import require_role
from lib.execptions import (
    ForbiddenException
)



@user_router.post("")
def create_user(
    user: NewUserSchema,
    db: Session = Depends(get_db_instance)
):

    service = UserService(db)

    return ApiResponse.success(
        data=service.create_user(user),
        message="User created successfully"
    )


@user_router.get("")
def get_all_users(
    current_user=Depends(
        require_role("admin")
    ),
    db: Session = Depends(get_db_instance)
):

    service = UserService(db)

    return ApiResponse.success(
        data=service.get_all_users(),
        message="Users fetched successfully"
    )


@user_router.get("/{user_id}")
def get_user_by_id(
    user_id: int,
    current_user=Depends(
        validate_jwt_token
    ),
    db: Session = Depends(get_db_instance)
):
    if (
    current_user["role"] != "admin"
    and
    current_user["user_id"] != user_id
):
        raise ForbiddenException(
        "Access denied"
    )
        
    
    

    service = UserService(db)

    return ApiResponse.success(
        data=service.get_user_by_id(
            user_id
        ),
        message="User fetched successfully"
    )


@user_router.put("/{user_id}")
def update_user(
    user_id: int,
    updated_user: NewUserSchema,
    current_user=Depends(
        validate_jwt_token
    ),
    db: Session = Depends(get_db_instance)
):
    if (
        current_user["role"] != "admin"
    and
    current_user["user_id"] != user_id


):
        raise ForbiddenException(
        "Access denied"
    )
        

    service = UserService(db)

    return ApiResponse.success(
        data=service.update_user(
            user_id,
            updated_user
        ),
        message="User updated successfully"
    )


@user_router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user=Depends(
        validate_jwt_token
    ),
    db: Session = Depends(get_db_instance)
):
    if (
    current_user["role"] != "admin"
    and
    current_user["user_id"] != user_id
):
        raise ForbiddenException(
            "Access denied"
        )

     
        
    service = UserService(db)

    service.delete_user(
        user_id
    )

    return ApiResponse.success(
        message="User deleted successfully"
    )

@user_router.patch(
    "/{user_id}/block"
)
def block_user(
    user_id: int,
    current_user=Depends(
        require_role("admin")
    ),
    db: Session = Depends(
        get_db_instance
    )
):

    service = UserService(db)

    return ApiResponse.success(
        data=service.block_user(
            user_id
        ),
        message="User blocked successfully"
    )