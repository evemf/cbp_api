# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
from dotenv import load_dotenv
from app.routes import routers  # Aseguramos la importación de los routers

# Cargar variables de entorno
load_dotenv()

# Instancia de FastAPI
app = FastAPI(title="Catalonia Blackball Party API")

# Middleware para permitir CORS (útil si usas frontend separado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción por dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers importados desde app.routes
for router in routers:
    app.include_router(router)

# Ruta para favicon.ico (mejor manejo de archivos)
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    static_dir = os.getenv("STATIC_DIR", "app/static")
    favicon_path = os.path.join(static_dir, "favicon.ico")

    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return JSONResponse(content={"error": "Favicon no encontrado"}, status_code=404)

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "API funcionando"}
