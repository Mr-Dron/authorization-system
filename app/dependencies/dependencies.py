from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

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

    