from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime

from datetime import datetime, timezone, timedelta

from app.db.database import Base
from app.config.settings import settings


class Tokens(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))