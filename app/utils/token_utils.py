from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Clave secreta (puedes obtenerla de variables de entorno)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
VERIFICATION_TOKEN_EXPIRE_MINUTES = 60  # Configura un tiempo de expiración apropiado para el token de verificación

# Función para crear un token de verificación
def create_verification_token(data: dict, expires_delta: timedelta = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": "verification"})  # Puedes añadir un campo para diferenciar el tipo de token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar el token de verificación
def verify_verification_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_token["type"] != "verification":
            raise JWTError("Invalid token type")
        return decoded_token
    except JWTError:
        raise JWTError("Token de verificación inválido o expirado.")
