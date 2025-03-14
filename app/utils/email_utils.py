# app/utils/email_utils.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración de correo
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_TLS") == "True",  # Corregido
    MAIL_SSL_TLS=os.getenv("MAIL_SSL") == "True",  # Corregido
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS") == "True",  # Asegurar autenticación
    VALIDATE_CERTS=os.getenv("VALIDATE_CERTS") == "True"  # Validar certificado
)


async def send_verification_email(email: str, token: str):
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8000")  # Valor por defecto si no está en .env
    verification_link = f"{frontend_url}/auth/verify/{token}"
    message = MessageSchema(
        subject="Verifica tu cuenta",
        recipients=[email],
        body=f"Por favor, haz clic en el siguiente enlace para verificar tu cuenta: {verification_link}",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)