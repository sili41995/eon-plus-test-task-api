from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class PhoneNumber(BaseModel):
    phone: str = Field(..., pattern=r"^\+\d{10,15}$")


class VerificationCode(BaseModel):
    phone: str = Field(..., pattern=r"^\+\d{10,15}$")
    code: str = Field(..., min_length=4, max_length=10, pattern=r"^\d+$")


class Message(BaseModel):
    id: int
    sender_id: int
    text: str
    date: datetime


class Chat(BaseModel):
    id: int
    name: str
    type: Literal["Chat", "Channel", "User"]


class SuccessConnectedMsg(BaseModel):
    success: bool


class ConnectedStatus(BaseModel):
    status: str
