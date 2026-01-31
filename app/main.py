from fastapi import FastAPI, status
from app.routers import *

app = FastAPI()

routers_list = [users.router]

for router in routers_list:
    app.include_router(router)

@app.get("/", status_code=status.HTTP_200_OK)
async def helloworld():
    return {"message": "hello world"}