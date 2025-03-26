from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from datetime import date
from app.models.user import User
from app.models.match import Match
from app.models.reservation import Reservation
from app.models.room import Room
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from app.schemas.room import RoomCreate, RoomUpdate
from app.schemas.user import UserCompleteProfile
from app.utils.security import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, limit: int = 10, offset: int = 0):
    return db.query(User).offset(offset).limit(limit).all()

def create_user(db: Session, email: str, hashed_password: str):
    try:
        new_user = User(email=email, hashed_password=hashed_password, role="user", is_verified=False)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear usuario: {e}")
        return None

def update_user(db: Session, user_id: int, update_data: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def complete_user_profile(db: Session, user: User, profile_data: UserCompleteProfile):
    if user.is_profile_complete:
        raise ValueError("El perfil ya está completo.")
    user.first_name = profile_data.first_name
    user.last_name = profile_data.last_name
    user.birth_date = profile_data.birth_date
    user.gender = profile_data.gender
    user.country = profile_data.country
    user.phone_number = profile_data.phone_number
    user.hashed_password = hash_password(profile_data.password)
    user.is_profile_complete = True
    user.is_active = True 
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}

def get_matches(db: Session):
    return db.query(Match).all()

def get_match(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()

def create_match(db: Session, match_data):
    try:
        new_match = Match(**match_data.dict())
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        return new_match
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear match: {e}")
        return None

def update_match_score(db: Session, match_id: int, new_score: dict):
    match = db.query(Match).filter(Match.id == match_id).first()
    if match:
        for key, value in new_score.items():
            setattr(match, key, value)
        db.commit()
        db.refresh(match)
        return match
    return None

def advance_round(db: Session, match_id: int):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return None
    match.round += 1
    db.commit()
    return match

def delete_match(db: Session, match_id: int):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return None
    db.delete(match)
    db.commit()
    return match

def is_room_available(db: Session, room_id: int, check_in: date, check_out: date) -> bool:
    overlapping_reservations = db.query(Reservation).filter(
        Reservation.room_id == room_id,
        and_(
            Reservation.check_in < check_out,
            Reservation.check_out > check_in
        )
    ).first()
    return overlapping_reservations is None

def create_reservation(db: Session, reservation_data: ReservationCreate):
    try:
        reservation = Reservation(**reservation_data.model_dump())
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear reserva: {e}")
        return None

def get_reservations(db: Session, user_id: int = None, limit: int = 10, offset: int = 0):
    query = db.query(Reservation)
    if user_id:
        query = query.filter(Reservation.user_id == user_id)
    return query.offset(offset).limit(limit).all()

def get_reservation(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def update_reservation(db: Session, reservation_id: int, update_data: ReservationUpdate):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(reservation, key, value)
    db.commit()
    db.refresh(reservation)
    return reservation

def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return None
    db.delete(reservation)
    db.commit()
    return reservation

def create_room(db: Session, room_data):
    try:
        new_room = Room(**room_data.dict())
        db.add(new_room)
        db.commit()
        db.refresh(new_room)
        return new_room
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear sala: {e}")
        return None

def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def get_rooms(db: Session, limit: int = 10, offset: int = 0):
    return db.query(Room).offset(offset).limit(limit).all()

def delete_room(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None
    db.delete(room)
    db.commit()
    return room

def update_available_rooms(db: Session):
    pass
