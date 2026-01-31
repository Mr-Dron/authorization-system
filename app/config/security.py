from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from app.config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context

def verify_password(plain_password: str, hashed_passwrod: str):
    return pwd_context.verify(plain_password, hashed_passwrod)

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
        raise ValueError("Invalid token")
    
    if payload["type"] != "access":
        raise ValueError("Invalid token")

    return payload