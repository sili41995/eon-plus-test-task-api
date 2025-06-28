from constants import errors, messages
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from services import hash_password, authenticate_user, create_access_token, get_db, get_current_user
from schemas import UserSignUp, Token, UserSignIn, UserOut
from models import User

router = APIRouter()


@router.post("/auth/sign-up", response_model=UserOut, status_code=201)
async def sign_up(user: UserSignUp, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.login == user.login))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=errors.EMAIL_ALREADY_USE)

    new_user = User(
        login=user.login,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/auth/sign-in", response_model=Token)
async def sign_in(user: UserSignIn, db: AsyncSession = Depends(get_db)):
    user_db = await authenticate_user(user.email, user.password, db)
    if not user_db:
        raise HTTPException(
            status_code=400, detail=errors.INCORRECT_CREDENTIALS)
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/sign-out")
async def get_profile(_=Depends(get_current_user)):
    return {"message": messages.SUCCESSFULLY_SIGN_OUT}


@router.get("/auth/current", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
