# app/utils/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Clave secreta para los tokens (debería estar en un archivo .env)
SECRET_KEY = "c9eab3219f27fd5c07ef604a5c59d773b71c8a02ab9baf8c7984315d94b3723a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Cifra una contraseña con bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña en texto plano contra su hash."""
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear un token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Genera un token JWT para autenticación."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Función para crear un token de verificación de email
def create_verification_token(email: str, expires_delta: timedelta = timedelta(hours=1)) -> str:
    """Crea un token JWT específico para la verificación de email."""
    return create_access_token(data={"sub": email, "type": "verify"}, expires_delta=expires_delta)

# Función para verificar un token (ya sea de autenticación o verificación de email)
def verify_token(token: str) -> str:
    """Verifica y decodifica un token JWT. Retorna el email si es válido."""
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
