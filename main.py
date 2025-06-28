from fastapi import FastAPI
from routers import authRouter, telegramRouter
from db import engine, Base
from dotenv import load_dotenv
import uvicorn
import os


load_dotenv()


PORT = os.getenv("PORT", 8000)


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(authRouter, prefix='/api')
app.include_router(telegramRouter, prefix='/api')


if __name__ == "__main__":
    port = int(PORT)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
