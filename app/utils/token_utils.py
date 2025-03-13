from datetime import datetime, timedelta
from jose import JWTError, jwt

# Clave secreta, debería ser una variable de entorno, pero para simplificar está fija aquí.
SECRET_KEY = "c9eab3219f27fd5c07ef604a5c59d773b71c8a02ab9baf8c7984315d94b3723a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Función para crear el token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
