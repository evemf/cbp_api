from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.room import RoomCreate, RoomRead
from app.crud import create_room, get_room, get_rooms, delete_room, update_available_rooms

# Definimos el prefijo de las rutas como "/rooms"
router = APIRouter(prefix="/rooms", tags=["rooms"])

# Endpoint para crear una nueva habitación
@router.post("/", response_model=RoomRead, tags=["rooms"])
def create_new_room(room: RoomCreate, db: Session = Depends(get_db)):
    return create_room(db, room)

# Endpoint para listar todas las habitaciones
@router.get("/", response_model=list[RoomRead], tags=["rooms"])
def list_rooms(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    rooms = get_rooms(db, skip=skip, limit=limit)
    return rooms

# Endpoint para obtener los detalles de una habitación específica
@router.get("/{room_id}", response_model=RoomRead, tags=["rooms"])
def get_room_detail(room_id: int, db: Session = Depends(get_db)):
    room = get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habitación no encontrada")
    return room

# Endpoint para reservar una habitación
@router.put("/{room_id}/reserve", response_model=RoomRead, tags=["rooms"])
def reserve_room(room_id: int, quantity: int, db: Session = Depends(get_db)):
    updated_room = update_available_rooms(db, room_id, quantity)
    if not updated_room:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay suficientes habitaciones disponibles")
    return updated_room

# Endpoint para eliminar una habitación por su ID
@router.delete("/{room_id}", response_model=dict, tags=["rooms"])
def delete_room_by_id(room_id: int, db: Session = Depends(get_db)):
    result = delete_room(db, room_id)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])
    return result
