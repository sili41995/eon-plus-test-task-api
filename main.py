from fastapi import FastAPI
from routers import authRouter
from db import engine, Base
import uvicorn


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(authRouter, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
