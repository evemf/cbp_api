from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.utils.token_utils import create_verification_token
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la conexión al servidor de correo
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_TLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL") == "True",
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS") == "True",
    VALIDATE_CERTS=os.getenv("VALIDATE_CERTS") == "True"
)

async def send_verification_email(email: str, verification_token: str):
    # Obtener la URL del backend desde las variables de entorno
    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")  # Valor por defecto si no se encuentra
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8080")  # Valor por defecto si no se encuentra
    
    # Crear el token de verificación
    verification_token = create_verification_token({"sub": email})
    
    # Construir el enlace de verificación
    verification_link = f"{frontend_url}/auth/verify?token={verification_token}"
    
    # Crear el mensaje para el correo
    message = MessageSchema(
        subject="Verifica tu cuenta",
        recipients=[email],
        body=f"<p>Haz clic en el siguiente enlace para verificar tu cuenta: <a href='{verification_link}'>Verificar</a></p>",
        subtype="html"
    )
    
    # Enviar el mensaje de verificación
    fm = FastMail(conf)
    await fm.send_message(message)
