from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    last_seen = Column(DateTime, index=True)
    is_active = Column(Boolean, default=True)

    groups_roles = relationship("GroupMembers", back_populates="user")
    created_groups = relationship("Groups", back_populates="creator")
    created_posts = relationship("Posts", back_populates="creator")