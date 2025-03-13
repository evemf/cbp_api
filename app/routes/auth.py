# app/routes/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin
from app.crud import get_user_by_email, create_user
from app.utils.security import verify_password, create_access_token, create_verification_token, verify_token
from app.utils.email_utils import send_verification_email

router = APIRouter()

# Esquemas para autenticación
class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

# Ruta para registrar al usuario
@router.post("/register", tags=["auth"])
async def register(user: UserRegister, db: Session = Depends(get_db)):
    # Verificar si el correo ya está registrado
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado.",
        )

    # Crear el usuario en la base de datos
    new_user = create_user(db, user)

    # Crear un token de verificación
    verification_token = create_verification_token(user.email)

    # Enviar el email de verificación
    await send_verification_email(user.email, verification_token)

    return {"message": f"Se ha enviado un email de verificación a {user.email}."}

# Ruta para verificar el correo electrónico del usuario
@router.get("/verify/{token}", tags=["auth"])
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        # Verificar el token de verificación
        email = verify_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado."
        )

    # Buscar al usuario por email
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    # Marcar la cuenta como activa
    user.is_active = True
    user.verification_token = None  # Limpiar el token de verificación
    db.commit()

    return {"message": "Cuenta verificada correctamente. Ya puedes iniciar sesión."}

# Ruta para login (iniciar sesión)
@router.post("/login", tags=["auth"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Buscar al usuario por email
    existing_user = get_user_by_email(db, user.username)
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar que la cuenta esté activa
    if not existing_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta inactiva. Revisa tu email y verifica tu cuenta."
        )

    # Crear el token de acceso (JWT)
    token = create_access_token({"sub": existing_user.email})

    return {"access_token": token, "token_type": "bearer"}
