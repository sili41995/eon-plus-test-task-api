from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    login: str
    email: EmailStr


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class UserSignUp(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
