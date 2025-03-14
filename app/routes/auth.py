from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse  
from fastapi import Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, CompleteProfile
from app.crud import get_user_by_email, create_user, complete_user_profile
from app.utils.security import verify_password, create_access_token, create_verification_token, verify_token
from app.utils.email_utils import send_verification_email
import os

router = APIRouter(prefix="/auth", tags=["auth"])

# 🔹 Registro con solo email
@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")

    new_user = create_user(db, user.email)
    verification_token = create_verification_token(user.email)

    await send_verification_email(user.email, verification_token)

    return {"message": f"Se ha enviado un email de verificación a {user.email}."}


FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080") 
@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    print(f"Token recibido: {token}") 
    try:
        email = verify_token(token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Token inválido o expirado: {str(e)}")
    
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    user.is_active = True
    db.commit()

    return RedirectResponse(url=f"{FRONTEND_URL}/complete-profile?token={token}", status_code=302)


# Completar perfil tras verificar email
@router.post("/complete-profile")
async def complete_profile(
    profile_data: CompleteProfile, 
    db: Session = Depends(get_db), 
    token: str = Header(None)  # Recibir el token en los headers
):
    if not token:
        raise HTTPException(status_code=400, detail="Token de autenticación requerido.")

    email = verify_token(token)  

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    updated_user = complete_user_profile(db, user.id, profile_data)

    return {"message": "Perfil completado con éxito.", "user": updated_user}

# 🔹 Login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not existing_user.is_active:
        raise HTTPException(status_code=403, detail="Cuenta inactiva. Revisa tu email y verifica tu cuenta.")

    token = create_access_token({"sub": existing_user.email})

    return {"access_token": token, "token_type": "bearer"}
