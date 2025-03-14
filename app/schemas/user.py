from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    email: EmailStr
    is_verified: bool
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None

class UserVerification(BaseModel):
    token: str

class UserCompleteProfile(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    country: str
    phone_number: str

class UserVerify(BaseModel):
    token: str