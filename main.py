from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI

import uvicorn

from auth import oauth2_scheme
from auth.views import router as auth_router

from db import db

from models import Base

from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await conn.close()

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(users_router)


@app.get('/')
def hello_index():
    return {
        'message': 'hello_index',
    }


@app.get('/items')
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
