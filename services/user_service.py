from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.User import User
from utils.bcrypt import bcrypt
import schemas.user


class UserService:

    def __init__(self, db: Session):
        self.db = db

    def find_user_by_email(self, email: str):

        return self.db.query(User).filter(
            User.email == email
        ).first()

    def create_user(
        self,
        user: schemas.user.NewUserSchema
    ):

        existing_user = self.find_user_by_email(
            user.email
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        new_user = User(
            name=user.name,
            email=user.email,
            password=bcrypt.hash(
                user.password
            )
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def get_all_users(self):

        return self.db.query(User).all()

    def get_user_by_id(
        self,
        user_id: int
    ):

        user = self.db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    def update_user(
        self,
        user_id: int,
        updated_user: schemas.user.NewUserSchema
    ):

        user = self.get_user_by_id(
            user_id
        )

        user.name = updated_user.name
        user.email = updated_user.email

        user.password = bcrypt.hash(
            updated_user.password
        )

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user(
        self,
        user_id: int
    ):

        user = self.get_user_by_id(
            user_id
        )

        self.db.delete(user)
        self.db.commit()

        return {
            "message": "User deleted successfully"
        }