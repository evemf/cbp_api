from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.models.reservation import Reservation

def is_room_available(db: Session, room_id: int, check_in: datetime, check_out: datetime) -> bool:
    """Verifica si la habitación está disponible en las fechas seleccionadas"""
    existing_reservations = db.query(Reservation).filter(
        Reservation.room_id == room_id,
        and_(
            Reservation.check_in < check_out, 
            Reservation.check_out > check_in   
        )
    ).first()
    
    return existing_reservations is None  

def create_reservation(db: Session, room_id: int, check_in: datetime, check_out: datetime):
    """Crea una reserva solo si la habitación está disponible"""
    if not is_room_available(db, room_id, check_in, check_out):
        raise ValueError("La habitación no está disponible en las fechas seleccionadas.")

    new_reservation = Reservation(room_id=room_id, check_in=check_in, check_out=check_out)
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation
