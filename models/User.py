from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from db.main import Base
from sqlalchemy import DateTime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name=Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True,nullable=False)
    role = Column(
    String(20),
    default="user"

                 )
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    otp = Column(
    String(10),
    nullable=True
    )
    otp_expiry = Column(
    DateTime,
    nullable=True
)
    reset_token = Column(
    String(500),
    nullable=True
)
    reset_token_expiry = Column(
    DateTime,
    nullable=True
)
    
