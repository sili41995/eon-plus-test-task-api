from fastapi import FastAPI
from routers import authRouter, telegramRouter
from db import engine, Base
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os


load_dotenv()


PORT = os.getenv("PORT", 8000)


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    'https://eon-plus-test-task.vercel.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authRouter, prefix='/api', tags=['Authentication'])
app.include_router(telegramRouter, prefix='/api', tags=['TG Chats'])


if __name__ == "__main__":
    port = int(PORT)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
