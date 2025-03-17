from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Cargar variables de entorno desde .env
load_dotenv()

# Clave secreta y algoritmo para los tokens
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 360

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

# Función para crear un token de verificación de correo
def create_verification_token(email: str, expires_delta: timedelta = timedelta(hours=1)) -> str:
    """Crea un token JWT específico para la verificación de email."""
    # Aquí, el 'type' es "verify" para asegurar que el token solo se use para verificación de correo
    token = create_access_token(data={"sub": email, "type": "verify"}, expires_delta=expires_delta)
    print(f"Token generado para {email}: {token}")  # Agrega esta línea para depuración
    return token

# Función para verificar un token (ya sea de autenticación o verificación de email)
def verify_token(token: str) -> str:
    """Verifica y decodifica un token JWT. Retorna el email si es válido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        # Verificamos que el tipo de token sea 'verify' para la verificación de email
        if token_type != "verify":
            raise InvalidTokenError("Tipo de token inválido")
        
        if email is None:
            raise InvalidTokenError("Token inválido")
        
        return email  

    except ExpiredSignatureError:
        raise InvalidTokenError("Token expirado")
    except InvalidTokenError:
        raise InvalidTokenError("Token inválido")
