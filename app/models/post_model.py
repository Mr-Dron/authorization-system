from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean

from app.db.database import Base

class Posts(Base):
    __tablename__ = "posts"

    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    create_at = Column(DateTime, nullable=False)

    is_active = Column(Boolean, default=True, index=True)

    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))

    creator = relationship("Users", back_populates="created_posts")
    group = relationship("Groups", back_populates="posts")