from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    email: EmailStr 

class UserCreate(UserBase):
    """Usado en el primer paso del registro (solo requiere email)."""
    pass 

class UserRead(UserBase):
    id: int
    is_verified: bool
    role: str
    is_profile_complete: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class UserCompleteProfile(BaseModel):
    """Usado cuando el usuario completa su perfil tras verificar su email."""
    password: str 
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    country: str
    phone_number: str

class UserUpdate(BaseModel):
    """Usado para la página de 'Perfil de usuario', permite modificar datos opcionales."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None

class UserVerify(BaseModel):
    """Modelo para manejar la verificación del usuario a través del token."""
    token: str
