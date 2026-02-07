from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from datetime import datetime

from app.db.database import Base


class Groups(Base):
    __tablename__ = "groups"

    title = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    create_at = Column(DateTime, default=datetime.now())

    is_active = Column(Boolean, default=True, index=True)

    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    creator = relationship("Users", back_populates="created_groups")
    members_roles = relationship("GroupMembers", back_populates="group")
    posts = relationship("Posts", back_populates="group")
