from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_room, get_room, get_rooms, delete_room, update_available_rooms
from app.schemas.room import RoomCreate, RoomUpdate  # Assegura't que aquests esquemes estan definits

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/")
def create_room_route(room: RoomCreate, db: Session = Depends(get_db)):
    new_room = create_room(db, room)
    if not new_room:
        raise HTTPException(status_code=400, detail="Error al crear sala")
    return new_room

@router.get("/")
def list_rooms(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_rooms(db, limit=limit, offset=skip)

@router.get("/{room_id}")
def read_room(room_id: int, db: Session = Depends(get_db)):
    room = get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return room

@router.delete("/{room_id}")
def delete_room_route(room_id: int, db: Session = Depends(get_db)):
    room = delete_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return {"message": "Sala eliminada correctamente"}

@router.put("/update-availability")
def update_rooms_availability(db: Session = Depends(get_db)):
    result = update_available_rooms(db)
    return result
