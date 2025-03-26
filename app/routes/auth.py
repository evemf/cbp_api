import os
import logging
from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Response, Request, Cookie, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin
from app.schemas.user import UserRead
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from app.crud import get_user_by_email, create_user
from app import services
from app.utils.security import verify_access_token, create_access_token, hash_password
from app.utils.email_utils import send_verification_email
from app.utils.token_utils import verify_verification_token, create_verification_token

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", "localhost")
VERIFICATION_TOKEN_EXPIRE_HOURS = 24

@router.post("/register")
async def register(user: UserRegister, response: Response, db: Session = Depends(get_db)):
    logger.debug("Registrando usuario con email: %s", user.email)
    
    # Verificar si el correo ya está registrado
    if get_user_by_email(db, user.email):
        logger.error("El correo electrónico ya está registrado: %s", user.email)
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
    
    # Crear el usuario con una contraseña temporal
    temp_password = "temporary"
    hashed_pw = hash_password(temp_password)
    new_user = create_user(db, user.email, hashed_pw)
    logger.debug("Usuario creado: %s", new_user.email)
    
    # Generar token de verificación
    verification_token = create_verification_token({"sub": new_user.email})
    
    # Enviar correo de verificación
    try:
        await send_verification_email(new_user.email, verification_token)
    except Exception as e:
        logger.error("Error al enviar el email de verificación: %s", str(e))
        raise HTTPException(status_code=500, detail="No se pudo enviar el correo de verificación.")
    
    # Establecer cookie para token de verificación
    response.set_cookie(
        key="verification_token",
        value=verification_token,
        httponly=True,
        secure=False,  # Cambiar a True en producción (HTTPS)
        samesite="Lax",
        max_age=VERIFICATION_TOKEN_EXPIRE_HOURS * 3600,
        domain=COOKIE_DOMAIN
    )
    
    return {"message": f"Se ha enviado un email de verificación a {new_user.email}."}

@router.get("/verify")
def verify_email(
    response: Response,
    token: str = Query(None),  # Token pasado en la URL
    verification_token: str = Cookie(None),  # O token en la cookie
    db: Session = Depends(get_db)
):
    # Priorizar el token de la query, sino usar el de la cookie
    actual_token = token or verification_token
    if not actual_token:
        raise HTTPException(status_code=400, detail="No se encontró token de verificación.")
    
    try:
        # Verificar el token de verificación
        email = verify_verification_token(actual_token)
    except Exception as e:
        logger.error("Error al verificar el token de verificación: %s", str(e))
        raise HTTPException(status_code=400, detail="Token de verificación inválido o expirado.")
    
    # Verificar si el usuario existe
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    # Marcar usuario como verificado
    user.is_verified = True
    db.commit()
    
    # Generar access_token
    access_token = create_access_token({"sub": user.email, "type": "access"})
    
    # Establecer la cookie de access_token (esto es lo que faltaba)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Cambiar a True en producción (HTTPS)
        samesite="None",  # Cambiar según tu configuración
        max_age=3600,
        domain=COOKIE_DOMAIN
    )
    
    # Eliminar cookie de verificación
    response.delete_cookie("verification_token")
    
    # Devolver JSON en lugar de redirección
    return {
        "message": "Cuenta verificada",
        "email": email,
        "redirect_url": f"{FRONTEND_URL}/complete-profile?email={email}"
    }


@router.post("/login")
async def login(response: Response, credentials: UserLogin, db: Session = Depends(get_db)):
    logger.debug("Intentando login para email: %s", credentials.email)
    user = services.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        logger.error("Credenciales inválidas para email: %s", credentials.email)
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token_data = {"sub": user.email, "type": "access"}
    token = create_access_token(token_data)
    logger.debug("Token de acceso generado: %s", token)
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Cambiar a True en producción (HTTPS)
        samesite="Lax",
        max_age=3600,
        path="/"
    )
    
    redirect_url = f"{FRONTEND_URL}/{'admin' if user.role=='admin' else 'dashboard'}"
    return {"message": "Inicio de sesión exitoso", "redirect_url": redirect_url, "user": UserRead.model_validate(user)}

@router.get("/me", response_model=UserRead)
def get_current_user(request: Request, db: Session = Depends(get_db), access_token: str = Cookie(None)):
    logger.debug("Accediendo a /auth/me con access_token: %s", access_token)
    
    if not access_token:
        logger.error("No se encontró access_token")
        raise HTTPException(status_code=401, detail="No autenticado")
    
    try:
        email = verify_access_token(access_token)
        logger.debug("Token de acceso decodificado, email: %s", email)
    except Exception as e:
        logger.error("Error al verificar access_token: %s", str(e))
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    user = get_user_by_email(db, email)
    if not user:
        logger.error("Usuario no encontrado para email: %s", email)
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    logger.debug("Usuario encontrado: %s", user.email)
    return UserRead.model_validate(user)

@router.post("/logout")
async def logout(response: Response):
    logger.debug("Logout solicitado")
    response.delete_cookie("access_token")
    return {"message": "Logout exitoso"}
