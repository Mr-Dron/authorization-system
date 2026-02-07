import asyncio

from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from app.routers import users, groups, posts, roles
from app.db.populating_db import filling_db
from app.tasks.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.db.database import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        await filling_db(db=session)
    
    task = asyncio.create_task(scheduler())

    yield

    task.cancel()


app = FastAPI(lifespan=lifespan)

routers_list = [users.router, groups.router, posts.router, roles.router]

for router in routers_list:
    app.include_router(router)

@app.get("/", status_code=status.HTTP_200_OK)
async def helloworld():
    return {"message": "hello world"}