# app/utils/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.utils.token_utils import SECRET_KEY, ALGORITHM

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Funciones de JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token de verificación
def create_verification_token(email: str, expires_delta: timedelta = timedelta(hours=1)):
    return create_access_token(data={"sub": email, "type": "verify"}, expires_delta=expires_delta)

# Verificar el token de verificación
def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if token_type != "verify":
            raise JWTError("Token inválido")
        if email is None:
            raise JWTError("Token inválido")
        return email
    except JWTError:
        raise JWTError("Token inválido o expirado")
