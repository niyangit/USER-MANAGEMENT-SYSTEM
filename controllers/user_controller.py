from fastapi import Depends
from sqlalchemy.orm import Session

from routes.user_route import user_router
from schemas.user import NewUserSchema, UserResponse
from db.main import get_db_instance
from services.user_service import UserService


@user_router.post("", response_model=UserResponse)
def create_user(
    user: NewUserSchema,
    db: Session = Depends(get_db_instance)
):

    service = UserService(db)

    return service.create_user(user)


@user_router.get("", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db_instance)
):

    service = UserService(db)

    return service.get_all_users()


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db_instance)
):

    service = UserService(db)

    return service.get_user_by_id(
        user_id
    )


@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    updated_user: NewUserSchema,
    db: Session = Depends(get_db_instance)
):

    service = UserService(db)

    return service.update_user(
        user_id,
        updated_user
    )


@user_router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db_instance)
):

    service = UserService(db)

    return service.delete_user(
        user_id
    )