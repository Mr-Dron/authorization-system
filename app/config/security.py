from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException

from app.config.settings import settings
from app.models.token_model import Tokens

import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

### пароли
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

### короткий токен
def create_access_token(user_id: int):
    
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": int(expire.timestamp())
    }

    encode_jwt = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    return encode_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Access token invalid or expire")
    
    if payload["type"] != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    return payload

### долгий токен 
async def create_refresh_token(user_id: int, db: AsyncSession) -> str:
    token = secrets.token_urlsafe(32)

    db_token = Tokens(user_id=user_id,
                      token=token)
    
    db.add(db_token)
    await db.commit()

    return token


async def verify_refresh_token(token: str, db: AsyncSession):

    db_token = (await db.execute(select(Tokens).where(Tokens.token == token))).scalar_one_or_none()

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    return db_token