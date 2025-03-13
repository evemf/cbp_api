from fastapi import FastAPI
from app.routes import routers

app = FastAPI()

for router in routers:
    app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "API funcionando"}
