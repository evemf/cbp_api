from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import (
    create_reservation,
    get_reservations,
    get_reservation,
    update_reservation,
    delete_reservation,
    is_room_available
)
from app.schemas.reservation import ReservationCreate, ReservationUpdate

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("/")
def create_reservation_route(reservation: ReservationCreate, db: Session = Depends(get_db)):
    if not is_room_available(db, reservation.room_id, reservation.check_in, reservation.check_out):
        raise HTTPException(status_code=400, detail="La habitación no está disponible en las fechas seleccionadas.")
    return create_reservation(db, reservation)

@router.get("/")
def get_reservations_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_reservations(db, limit=limit, offset=skip)

@router.get("/{reservation_id}")
def get_reservation_route(reservation_id: int, db: Session = Depends(get_db)):
    reserva = get_reservation(db, reservation_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")
    return reserva

@router.put("/{reservation_id}")
def update_reservation_route(reservation_id: int, reservation_data: ReservationUpdate, db: Session = Depends(get_db)):
    reserva_actualizada = update_reservation(db, reservation_id, reservation_data)
    if not reserva_actualizada:
        raise HTTPException(status_code=404, detail="No se pudo actualizar la reserva, puede que no exista.")
    return reserva_actualizada

@router.delete("/{reservation_id}")
def delete_reservation_route(reservation_id: int, db: Session = Depends(get_db)):
    success = delete_reservation(db, reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="No se pudo eliminar la reserva, puede que no exista.")
    return {"message": "Reserva eliminada correctamente"}
