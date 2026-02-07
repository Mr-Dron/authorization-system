from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.dependencies import get_session, get_current_user_with_activity, set_user_status
from app.schemas import user_schemas
from app.services import user_service
from app.models.user_model import Users

router = APIRouter(prefix="/users", tags=["User"])

# регистрация 
@router.post("/registration/", status_code=status.HTTP_201_CREATED)
async def user_create(user_data: user_schemas.UserRegistration, db: AsyncSession=Depends(get_session)):
    return await user_service.create_user(user_data=user_data, db=db)


# вход в аккаунт
@router.post("/login/", status_code=status.HTTP_200_OK)
async def user_login(login_data: user_schemas.UserLogin, db: AsyncSession=Depends(get_session)):
    return await user_service.login_user(login_data=login_data, db=db)

# вход в аккаунт для swagger (для теста)
# @router.post("/login/swag/", status_code=status.HTTP_200_OK)
# async def user_login(login_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession=Depends(get_session)):
#     print(login_data.username)
#     return await user_service.login_user_swag(login_data=login_data, db=db)

# обновление пользователя
@router.put("/update/", response_model=user_schemas.UserOut, status_code=status.HTTP_200_OK,
            dependencies=[Depends(set_user_status(True))])
async def user_update(user_data: user_schemas.UserUpdate, current_user: Users=Depends(get_current_user_with_activity), db: AsyncSession=Depends(get_session)):
    return await user_service.update_user(user_data=user_data, current_user=current_user, db=db)

# выход из аккаунта
@router.post("/logout/", status_code=status.HTTP_200_OK, 
             dependencies=[Depends(set_user_status(False))])
async def user_logout(refresh_token: str, db: AsyncSession=Depends(get_session)):
    return await user_service.logout_user(refresh_token=refresh_token, db=db)

# удаление аккаунта
@router.delete("/", status_code=status.HTTP_200_OK,
               dependencies=[Depends(set_user_status(False))])
async def user_delete(current_user: Users=Depends(get_current_user_with_activity), db: AsyncSession=Depends(get_session)):
    return await user_service.delete_user(current_user=current_user, db=db)

# обновление токена
@router.post("/refresh/", status_code=status.HTTP_200_OK)
async def refresh(refresh_token: str, db: AsyncSession=Depends(get_session)):
    return await user_service.refresh_access_token(refresh_token=refresh_token, db=db)