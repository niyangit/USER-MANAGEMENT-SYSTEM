from sqlalchemy.orm import Session

from models.User import User
from utils.bcrypt import bcrypt
import schemas.user

from lib.execptions import (
    NotFoundException,
    ConflictException,
    InternalServerException,
    AuthenticationException
)

from utils.cache import (
    user_cache,
    users_cache
)


class UserService:

    def __init__(self, db: Session):
        self.db = db

    def find_user_by_email(
        self,
        email: str,
        raise_exception: bool = False
    ):

        user = self.db.query(User).filter(
            User.email == email
        ).first()

        if not user and raise_exception:
            raise NotFoundException(
                f"User with email '{email}' not found"
            )

        return user

    def create_user(
        self,
        user: schemas.user.NewUserSchema
    ):

        exist_user = self.find_user_by_email(
            user.email
        )

        if exist_user:
            raise ConflictException(
                "Email already exists"
            )

        try:

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

            users_cache.clear()

            return new_user

        except Exception as e:

            self.db.rollback()

            raise InternalServerException(
                str(e)
            )

    def get_all_users(self):

        cache_key = "all_users"

        if cache_key in users_cache:

            print(
                "ALL USERS CACHE HIT"
            )

            return users_cache[
                cache_key
            ]

        print(
            "ALL USERS DB HIT"
        )

        try:

            users = self.db.query(
                User
            ).all()

            users_cache[
                cache_key
            ] = users

            return users

        except Exception as e:

            raise InternalServerException(
                str(e)
            )

    def get_user_by_id(
        self,
        user_id: int
    ):

        cache_key = f"user:{user_id}"

        if cache_key in user_cache:

            print(
                "CACHE HIT"
            )

            return user_cache[
                cache_key
            ]

        print(
            "DB HIT"
        )

        user = self.db.query(
            User
        ).filter(
            User.id == user_id
        ).first()

        if not user:

            raise NotFoundException(
                f"User with id {user_id} not found"
            )

        user_cache[
            cache_key
        ] = user

        return user

    def update_user(
        self,
        user_id: int,
        updated_user: schemas.user.NewUserSchema
    ):

        user = self.get_user_by_id(
            user_id
        )

        existing_user = self.db.query(
            User
        ).filter(
            User.email == updated_user.email,
            User.id != user_id
        ).first()

        if existing_user:

            raise ConflictException(
                "Email already exists"
            )

        try:

            user.name = updated_user.name
            user.email = updated_user.email

            user.password = bcrypt.hash(
                updated_user.password
            )

            self.db.commit()
            self.db.refresh(user)

            user_cache.pop(
                f"user:{user_id}",
                None
            )

            users_cache.clear()

            return user

        except Exception as e:

            self.db.rollback()

            raise InternalServerException(
                str(e)
            )

    def delete_user(
        self,
        user_id: int
    ):

        user = self.get_user_by_id(
            user_id
        )

        try:

            self.db.delete(user)
            self.db.commit()

            user_cache.pop(
                f"user:{user_id}",
                None
            )

            users_cache.clear()

            return {
                "message":
                "User deleted successfully"
            }

        except Exception as e:

            self.db.rollback()

            raise InternalServerException(
                str(e)
            )

    def block_user(
        self,
        user_id: int
    ):

        user = self.get_user_by_id(
            user_id
        )

        user.is_active = False

        self.db.commit()

        self.db.refresh(user)

        user_cache.pop(
            f"user:{user_id}",
            None
        )

        users_cache.clear()

        return user