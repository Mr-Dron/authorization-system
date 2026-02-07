from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from datetime import datetime, timezone

from app.db.database import AsyncSessionLocal
from app.models import Users, Tokens
from app.config.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

# контекст менеджер сессии
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal () as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

# получение текущего пользователя 
async def get_current_user(token: str=Depends(oauth2_scheme),
                           db: AsyncSession=Depends(get_session)) -> Users:

    payload = verify_access_token(token)
    
    user_id = payload["sub"]

    current_user = (await db.execute(select(Users).where(Users.id == user_id))).scalar_one_or_none()

    if not current_user:
        raise ValueError("Invalid user data")

    return current_user

#получение текущего пользователя с обновлением активности
def get_current_user_with_activity():
    async def dependency(user: Users=Depends(get_current_user),
                         db: AsyncSession=Depends(get_session)):
        await update_last_seen(user=user, db=db)
        return user
    return dependency

#обновление активности пользователя
async def update_last_seen(user: Users, db: AsyncSession):

    user.last_seen = datetime.now(timezone.utc)

    db.add(user)
    await db.commit()

    return {"message", "ok"}

#фабрика зависимостей на изменение состояние пользователя
def set_user_status(state: bool):
    async def inner(user: Users=Depends(get_current_user),
                    db: AsyncSession=Depends(get_session)):
        
        if user.online != state:
            user.online = state

            db.add(user)
            await db.commit()
            
        return {"message": "ok"} 
    return inner
    