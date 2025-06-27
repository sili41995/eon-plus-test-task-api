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


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Render використовує PORT із env
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
