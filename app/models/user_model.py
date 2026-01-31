from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Text

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)