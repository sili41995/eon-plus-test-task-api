from pydantic import BaseModel, Field


class PhoneNumber(BaseModel):
    phone: str = Field(..., pattern=r"^\+\d{10,15}$")


class VerificationCode(BaseModel):
    phone: str = Field(..., pattern=r"^\+\d{10,15}$")
    code: str = Field(..., min_length=4, max_length=10, pattern=r"^\d+$")
