from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno desde .env

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

try:
    # Intentamos conectar a la base de datos
    with engine.connect() as connection:
        print("Conexión exitosa a la base de datos")
except Exception as e:
    print("Error al conectar con la base de datos:", e)
