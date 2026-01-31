from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, status, Depends

from app.dependencies.dependencies import get_session, get_current_user, get_token
from app.schemas import user_schemas
from app.services import user_service
from app.models.user_model import Users

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/registration/", status_code=status.HTTP_201_CREATED)
async def user_create(user_data: user_schemas.UserRegistration, db: AsyncSession=Depends(get_session)):
    return await user_service.create_user(user_data=user_data, db=db)


@router.post("/login/", status_code=status.HTTP_200_OK)
async def user_login(login_data: user_schemas.UserLogin, db: AsyncSession=Depends(get_session)):
    return await user_service.login_user(login_data=login_data, db=db)


@router.put("/update/", response_model=user_schemas.UserOut, status_code=status.HTTP_200_OK)
async def user_update(user_data: user_schemas.UserUpdate, current_user: Users=Depends(get_current_user), db: AsyncSession=Depends(get_session)):
    return await user_service.update_user(user_data=user_data, current_user=current_user, db=db)


@router.get("/logout/", status_code=status.HTTP_200_OK)
async def user_logout(token: str=Depends(get_token), db: AsyncSession=Depends(get_session)):
    return await user_service.logout_user(token=token, db=db)


@router.delete("", status_code=status.HTTP_200_OK)
async def user_delete(current_user: Users=Depends(get_current_user), db: AsyncSession=Depends(get_session)):
    return await user_service.delete_user(current_user=current_user, db=db)