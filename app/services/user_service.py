from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from fastapi import HTTPException

from app.schemas import user_schemas
from app.dependencies.dependencies import set_user_status
from app.models import Users, Tokens
from app.config import security


async def create_user(user_data: user_schemas.UserRegistration, db: AsyncSession):

    hashed_pass = security.hash_password(user_data.password)
    data = user_data.model_dump()

    data.pop("password")
    data.pop("repeated_password")

    data["hashed_password"] = hashed_pass

    new_user = Users(**data)

    db.add(new_user)

    return {"message": "user created"}


async def login_user(login_data: user_schemas.UserLogin, db: AsyncSession):

    stmt = (
        select(Users)
        .where(Users.email == login_data.email)
    )

    user = (await db.execute(stmt)).scalar_one_or_none()

    if (not user or 
        not security.verify_password(login_data.password, user.hashed_password) or 
        user.is_active):
        raise HTTPException(status_code=400, detail="Login error")
    
    
    access_token = security.create_access_token(user.id)
    refresh_token = await security.create_refresh_token(user_id=user.id, db=db)

    await set_user_status(state=True)(user=user, db=db)

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "type_token": "bearer"}

# функция для тестирования через swagger
# async def login_user_swag(login_data: user_schemas.UserLoginSwag, db: AsyncSession):

#     stmt = (
#         select(Users)
#         .where(Users.email == login_data.username)
#     )

#     user = (await db.execute(stmt)).scalar_one_or_none()

#     if (not user or 
#         not security.verify_password(login_data.password, user.hashed_password) or 
#         user.is_active):
#         raise HTTPException(status_code=400, detail="Login error")
    
    
#     access_token = security.create_access_token(user.id)
#     refresh_token = await security.create_refresh_token(user_id=user.id, db=db)

#     await set_user_status(state=True)(user=user, db=db)

#     return {"access_token": access_token,
#             "refresh_token": refresh_token,
#             "type_token": "bearer"}


async def update_user(user_data: user_schemas.UserUpdate, current_user: Users, db: AsyncSession):

    new_data = user_data.model_dump(exclude_unset=True)

    stmt = (
        update(Users)
        .values(**new_data)
        .where(Users.id == current_user.id)
        .returning(Users)
    )

    updated_user = (await db.execute(stmt)).scalar_one_or_none()

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found error")
    
    return updated_user


async def logout_user(refresh_token: str, db: AsyncSession):

    stmt = (delete(Tokens)
            .where(Tokens.token == refresh_token))
    
    result = await db.execute(stmt)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=401, detail="Token not found")
    
    return {"message": "Logged out successfully"}


async def delete_user(current_user: Users, db: AsyncSession):

    #выход со всех устройств
    stmt = (
        delete(Tokens)
        .where(Tokens.user_id == current_user.id)
        .returning(Tokens)
    )

    await db.execute(stmt)

    current_user.is_active = False

    db.add(current_user)
    await db.commit
    
    return {"message": "user deleted"}


async def refresh_access_token(refresh_token: str, db: AsyncSession):

    token_data = await security.verify_refresh_token(token=refresh_token, db=db)

    access_token = security.create_access_token(user_id=token_data.user_id)

    return {"access_token": access_token,
            "type_token": "bearer"}