from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
import uuid
from app.models.user import User
from app.models.competition import Competition
from app.models.room import Room
from app.models.reservation import Reservation
from app.models.match import Match
from app.schemas.user import UserCreate, UserUpdate, UserCompleteProfile
from app.schemas.competition import CompetitionCreate
from app.schemas.room import RoomCreate
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from app.schemas.match import MatchCreate, MatchUpdateScore
from app.utils.security import hash_password
from app.utils.utils import calculate_total_price
from app.utils.email_utils import send_verification_email

def create_user(db: Session, email: str):
    verification_token = str(uuid.uuid4())
    db_user = User(email=email, verification_token=verification_token, is_verified=False, is_profile_complete=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    send_verification_email(email, verification_token)
    return db_user

def verify_email(db: Session, token: str):
    user = db.query(User).filter(User.verification_token == token).first()
    if user:
        user.is_verified = True
        user.verification_token = None
        db.commit()
        db.refresh(user)
        return user
    return None

def complete_user_profile(db: Session, user_id: int, profile_data: UserCompleteProfile):
    user = db.query(User).filter(User.id == user_id, User.is_verified == True).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no verificado")

    user.hashed_password = hash_password(profile_data.password)
    user.first_name = profile_data.first_name
    user.last_name = profile_data.last_name
    user.birth_date = profile_data.birth_date
    user.gender = profile_data.gender
    user.country = profile_data.country
    user.phone_number = profile_data.phone_number
    user.is_profile_complete = True
    
    db.commit()
    db.refresh(user)

    return user 

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        db.flush() 
        return {"message": "Usuario eliminado correctamente"}
    return {"error": "Usuario no encontrado"}

def create_match(db: Session, match_data: MatchCreate):
    db_match = Match(**match_data.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def get_matches(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Match).offset(skip).limit(limit).all()

def get_match(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()

def update_match_score(db: Session, match_id: int, score_data: MatchUpdateScore):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return None

    for key, value in score_data.model_dump(exclude_unset=True).items():
        setattr(match, key, value)

    db.commit()
    db.refresh(match)
    return match

def advance_round(db: Session, match_id: int):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return None

    # Aquí iría la lógica para avanzar de ronda, dependiendo de tu modelo de negocio
    match.round += 1  

    db.commit()
    db.refresh(match)
    return match

def delete_match(db: Session, match_id: int):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return None  # O podrías lanzar una excepción

    db.delete(match)
    db.commit()
    return {"message": "Partido eliminado correctamente"}

def get_reservations(db: Session, skip: int = 0, limit: int = 10):
    """Obtiene todas las reservas con paginación."""
    return db.query(Reservation).offset(skip).limit(limit).all()

def get_reservation(db: Session, reservation_id: int):
    """Obtiene una reserva específica por su ID."""
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def create_reservation(db: Session, reservation_data: ReservationCreate):
    """Crea una nueva reserva."""
    db_reservation = Reservation(**reservation_data.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def update_reservation(db: Session, reservation_id: int, reservation_data: ReservationUpdate):
    """Actualiza una reserva existente."""
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        return None
    
    for key, value in reservation_data.dict(exclude_unset=True).items():
        setattr(db_reservation, key, value)
    
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def delete_reservation(db: Session, reservation_id: int):
    """Elimina una reserva si existe."""
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        return False
    
    db.delete(db_reservation)
    db.commit()
    return True

def is_room_available(db: Session, room_id: int, check_in: datetime, check_out: datetime):
    """Verifica si una habitación está disponible en un rango de fechas."""
    overlapping_reservations = (
        db.query(Reservation)
        .filter(
            Reservation.room_id == room_id,
            Reservation.check_out > check_in,
            Reservation.check_in < check_out
        )
        .count()
    )
    return overlapping_reservations == 0

def create_room(db: Session, room_data: RoomCreate):
    new_room = Room(**room_data.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def get_rooms(db: Session):
    return db.query(Room).all()

def delete_room(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room:
        db.delete(room)
        db.commit()
        return True
    return False

def update_available_rooms(db: Session, room_id: int, new_available: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room:
        room.available_rooms = new_available
        db.commit()
        db.refresh(room)
        return room
    return None