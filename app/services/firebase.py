import firebase_admin
from firebase_admin import credentials, messaging
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la ruta del archivo de credenciales de Firebase
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not cred_path or not os.path.exists(cred_path):
    print("Error: No se encontró el archivo de credenciales de Firebase.")
else:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Firebase inicializado correctamente.")
    except Exception as e:
        print(f"Error al inicializar Firebase: {e}")

def send_push_notification(token, title, body):
    """Función para enviar notificaciones push"""
    if not firebase_admin._apps:
        print("Firebase no está inicializado. No se pueden enviar notificaciones.")
        return

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    # Enviar la notificación
    try:
        response = messaging.send(message)
        print(f"Notificación enviada con éxito: {response}")
    except Exception as e:
        print(f"Error al enviar la notificación: {e}")
