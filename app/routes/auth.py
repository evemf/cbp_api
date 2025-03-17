import os
from fastapi import APIRouter, HTTPException, Response, Request, Cookie, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin
from app.schemas.user import UserRead
import jwt  # <--- Agrega esta línea si falta
from jwt import ExpiredSignatureError, InvalidTokenError
from app.crud import get_user_by_email, create_user, authenticate_user
from app.utils.security import verify_token, create_access_token
from app.utils.email_utils import send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", "localhost")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
    new_user = create_user(db, user.email)
    await send_verification_email(new_user.email, new_user.verification_token, backend_url=BACKEND_URL)
    return {"message": f"Se ha enviado un email de verificación a {new_user.email}."}

@router.get("/verify/{token}")
def verify_email(token: str, response: Response, db: Session = Depends(get_db)):
    try:
        email = verify_token(token)
    except Exception:
        raise HTTPException(status_code=400, detail="Token inválido o expirado.")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if not user.is_verified:
        user.is_verified = True
        db.commit()
    redirect_url = f"{FRONTEND_URL}/complete-profile?email={email}"
    res = JSONResponse(content={"message": "Email verificado", "redirect_url": redirect_url, "email": email})
    res.set_cookie(
        key="verification_token",
        value=token,
        httponly=True,
        secure=False,       # En producción, usa True si se usa HTTPS
        samesite="Lax",
        max_age=600,
        domain=COOKIE_DOMAIN  # Aquí usamos la variable de entorno
    )
    return res

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Verificar que las variables de entorno están configuradas correctamente
if not SECRET_KEY or not ALGORITHM:
    raise ValueError("SECRET_KEY o ALGORITHM no están configurados en el archivo .env")

@router.get("/me")
def get_current_user(request: Request, access_token: str = Cookie(None)):
    print(f"🔍 Cookies recibidas: {request.cookies}")

    if not access_token:
        print("❌ No se encontró el token en las cookies")
        raise HTTPException(status_code=401, detail="No autenticado")

    print(f"🔑 Token leído de la cookie: {access_token}")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("✅ Token válido:", payload)
        return {"message": "Token válido", "user": payload}
    except jwt.ExpiredSignatureError:
        print("❌ Token expirado")
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        print("❌ Token inválido")
        raise HTTPException(status_code=401, detail="Token inválido")


@router.post("/login")
async def login(response: Response, credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token_data = {"sub": user.email, "type": "access"}
    token = create_access_token(data=token_data)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600,
        path="/"
    )

    # Redirección manual al frontend
    frontend_redirect_url = f"{FRONTEND_URL}/dashboard"
    return {"message": "Inicio de sesión exitoso", "redirect_url": frontend_redirect_url}



