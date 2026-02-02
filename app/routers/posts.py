from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

from app.dependencies.permissions_validators import check_permission
from app.dependencies.dependencies import get_session, get_current_user
from app.schemas import post_schemas
from app.models import *
from app.services import post_service

route = APIRouter(prefix="/group/{group_id}/posts", tags=["Posts"])

@route.post("/", response_model=post_schemas.PostOutFull, status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(check_permission(2))])
async def create_post(group_id: int, post_data: post_schemas.PostCreate, current_user: Users=Depends(get_current_user), db: AsyncSession=Depends(get_session)):
    return await post_service.create_post(group_id=group_id, post_data=post_data, current_user=current_user, db=db)

@route.put("/{post_id}/", response_model=post_schemas.PostOutFull, status_code=status.HTTP_200_OK,
           dependencies=[Depends(check_permission(2))])
async def update_post(group_id: int, post_id: int, post_data: post_schemas.PostUpdate, db: AsyncSession=Depends(get_session)):
    return await post_service.update_post(post_id=post_id, post_data=post_data, db=db)

@route.delete("/{post_id}/", status_code=status.HTTP_200_OK,
              dependencies=[Depends(check_permission(2))])
async def delete_post(group_id: int, post_id: int, db: AsyncSession=Depends(get_session)):
    return await post_service.delete_post(post_id=post_id, db=db)

@route.get("/", response_model=post_schemas.PostOutFull, status_code=status.HTTP_200_OK)
async def get_posts(group_id: int, db: AsyncSession):
    return await post_service.get_all_posts_in_group(group_id=group_id, db=db)