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
    MAIL_STARTTLS=True,  # Incluir TLS
    MAIL_SSL_TLS=False,  # No usar SSL
)

async def send_verification_email(email: str, token: str):
    verification_link = f"http://localhost:8000/auth/verify/{token}"
    message = MessageSchema(
        subject="Verifica tu cuenta",
        recipients=[email],
        body=f"Por favor, haz clic en el siguiente enlace para verificar tu cuenta: {verification_link}",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
