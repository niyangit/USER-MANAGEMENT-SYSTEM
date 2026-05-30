from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from db.main import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name=Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True,nullable=False)
    department=Column(String(100))
    
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)