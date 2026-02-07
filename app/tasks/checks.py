from sqlalchemy import update, select

from datetime import datetime, timezone, timedelta

from app.db.database import AsyncSessionLocal
from app.models import Users, Tokens
from app.config.settings import settings
from app.services.user_service import logout_user


async def check_user_last_seen():
    async with AsyncSessionLocal() as db: 
        stmt = (
            update(Users)
            .where(Users.last_seen > datetime.now(timezone.utc) + timedelta(minutes=settings.TIME_SINCE_LAST_REQUEST))
            .values(online=False)
        )

        await db.execute(stmt)
        await db.commit()


async def logout_inactive_users():
    async with AsyncSessionLocal() as db:
        cutoff = datetime.now(timezone.utc) - timedelta(days=settings.REFRESH_TOKEN)
        
        stmt = (
            select(Tokens)
            .join(Users, Users.id == Tokens.user_id)
            .where(Users.last_seen < cutoff)
        )

        tokens = (await db.execute(stmt)).scalars().all()

        for token in tokens:
            await logout_user(refresh_token=token.token, db=db)