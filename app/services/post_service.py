from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from fastapi import HTTPException

from app.models import *
from app.schemas import post_schemas

async def create_post(group_id: int, post_data: post_schemas.PostCreate, current_user: Users, db: AsyncSession):

    data = post_data.model_dump()
    data["creator_id"] = current_user.id
    data["group_id"] = group_id

    new_post = Posts(**data)

    db.add(new_post)

    await db.flush()
    await db.refresh(new_post)

    return new_post


async def update_post(post_id: int, post_data: post_schemas.PostUpdate, db: AsyncSession):

    data = post_data.model_dump()

    stmt = (
        update(Posts)
        .values(**data)
        .where(Posts.id == post_id)
        .returning(Posts)
    )

    updated_post = (await db.execute(stmt)).scalar_one_or_none()

    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return updated_post

async def delete_post(post_id: int, db: AsyncSession):

    stmt = (
        delete(Posts)
        .where(Posts.id == post_id)
        .returning(Posts)
    )

    deleted_post = (await db.execute(stmt)).scalar_one_or_none()

    if not deleted_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {"message": "post delete successfully"}

async def get_all_posts_in_group(group_id: int, db: AsyncSession):
    
    stmt = (
        select(Posts)
        .where(Posts.group_id == group_id)
    )

    posts = (await db.execute(stmt)).scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    
    return posts