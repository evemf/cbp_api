from fastapi import APIRouter
from app.services.firebase import send_push_notification

router = APIRouter()

@router.post("/send-notification/")
def send_notification(token: str, title: str, body: str):
    """Endpoint para enviar notificaciones push"""
    send_push_notification(token, title, body)
    return {"message": "Notificación enviada"}