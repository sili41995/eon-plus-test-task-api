from constants import errors
from dotenv import load_dotenv
from models.user import User
from schemas import PhoneNumber, VerificationCode, Message, Chat, SuccessConnectedMsg, ConnectedStatus
from fastapi import APIRouter, Depends, HTTPException
from services import get_current_user
from telethon import TelegramClient
from typing import List
import re
import os
import logging


load_dotenv()


logger = logging.getLogger("telegram")


API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

router = APIRouter()


user_telegram_sessions = {}


@router.post("/telegram/connect")
async def telegram_connect(data: PhoneNumber, user: User = Depends(get_current_user)) -> ConnectedStatus:
    username = user.login

    session_dir = "sessions"
    os.makedirs(session_dir, exist_ok=True)
    session_name = os.path.join(session_dir, f"session_{username}")

    client = TelegramClient(session_name, API_ID, API_HASH)
    await client.connect()
    user_telegram_sessions[username] = client

    if not await client.is_user_authorized():
        await client.send_code_request(data.phone)
        return {"status": "code_sent"}

    return {"status": errors.ALREADY_AUTH}


@router.post("/telegram/verify")
async def telegram_verify(data: VerificationCode, user: User = Depends(get_current_user)) -> SuccessConnectedMsg:
    username = user.login
    client = user_telegram_sessions.get(username)
    if not client:
        raise HTTPException(status_code=400, detail=errors.SESSION_NOT_FOUND)

    try:
        await client.sign_in(data.phone, data.code)
        logger.info(f"User {username} verified Telegram code")
        return {"success": True}
    except Exception as e:
        logger.error(f"{errors.VERIFICATION_FAILED}: {e}")
        raise HTTPException(status_code=400, detail=errors.INVALID_CODE)


@router.get("/telegram/chats")
async def get_chats(user: User = Depends(get_current_user)) -> List[Chat]:
    username = user.login
    client = user_telegram_sessions.get(username)

    if not client or not await client.is_user_authorized():
        raise HTTPException(status_code=400, detail=errors.TG_NOT_CONNECTED)

    dialogs = await client.get_dialogs()
    return [
        {"id": dialog.id, "name": dialog.name,
            "type": type(dialog.entity).__name__}
        for dialog in dialogs if dialog.name
    ]


@router.get("/telegram/messages/{chat_id}")
async def get_messages(chat_id: int, user: User = Depends(get_current_user)) -> Message:
    username = user.login
    client = user_telegram_sessions.get(username)

    if not client or not await client.is_user_authorized():
        raise HTTPException(status_code=400, detail=errors.TG_NOT_CONNECTED)

    try:
        messages = []
        async for message in client.iter_messages(chat_id, limit=30):
            messages.append({
                "id": message.id,
                "sender_id": message.sender_id,
                "text": message.message,
                "date": str(message.date)
            })
        return messages[::-1]
    except Exception as e:
        logger.error(f"{errors.MSG_NOT_FOUND}: {e}")
        raise HTTPException(status_code=500, detail=errors.MSG_NOT_FOUND)
