import firebase_admin
from firebase_admin import credentials, messaging
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno necesarias
firebase_config = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
}

# Validar si la clave privada está presente antes de inicializar Firebase
if not firebase_config["private_key"]:
    print("Advertencia: FIREBASE_PRIVATE_KEY no está configurada. Firebase no se inicializará.")
else:
    try:
        # Inicializar Firebase solo si las credenciales son válidas
        cred = credentials.Certificate(firebase_config)
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
