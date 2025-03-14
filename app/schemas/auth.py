from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Primer paso del registro (solo email)
class UserRegister(BaseModel):
    email: EmailStr

# Segundo paso: completar perfil después de verificar el email
class CompleteProfile(BaseModel):
    password: str
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    country: str
    phone_number: str

# Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
