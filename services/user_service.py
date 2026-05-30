

from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.User import User
import schemas.user


class UserService:

    @staticmethod
    def find_user_by_email(email: str, db: Session):

        return db.query(User).filter(
            User.email == email
        ).first()

    @staticmethod
    def create_user(user: schemas.user.NewUserSchema, db: Session):

        existing_user = UserService.find_user_by_email(
            user.email,
            db
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        new_user = User(
            name=user.name,
            email=user.email,
            password=user.password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def get_all_users(db: Session):

        return db.query(User).all()

    @staticmethod
    def get_user_by_id(user_id: int, db: Session):

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    @staticmethod
    def update_user(
        user_id: int,
        updated_user: schemas.user.NewUserSchema,
        db: Session
    ):

        user = UserService.get_user_by_id(
            user_id,
            db
        )

        user.name = updated_user.name
        user.email = updated_user.email
        user.password = updated_user.password

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_user(
        user_id: int,
        db: Session
    ):

        user = UserService.get_user_by_id(
            user_id,
            db
        )

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully"
        }