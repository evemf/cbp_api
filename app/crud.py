from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.models.user import User
from app.models.competition import Competition
from app.models.room import Room
from app.models.reservation import Reservation
from app.models.match import Match
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.competition import CompetitionCreate
from app.schemas.room import RoomCreate
from app.schemas.match import MatchCreate, MatchUpdateScore
from app.utils.security import hash_password
from app.utils.utils import calculate_total_price 



# --- USER FUNCTIONS ---
def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "Usuario eliminado correctamente"}
    return {"error": "Usuario no encontrado"}

# --- COMPETITION FUNCTIONS ---
def get_competitions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Competition).offset(skip).limit(limit).all()

def get_competition(db: Session, competition_id: int):
    return db.query(Competition).filter(Competition.id == competition_id).first()

def create_competition(db: Session, competition: CompetitionCreate):
    db_competition = Competition(name=competition.name, description=competition.description)
    db.add(db_competition)
    db.commit()
    db.refresh(db_competition)
    return db_competition

# --- ROOM FUNCTIONS ---
def create_room(db: Session, room: RoomCreate):
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_rooms(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Room).offset(skip).limit(limit).all()

def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def update_available_rooms(db: Session, room_id: int, quantity: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room and room.available_rooms >= quantity:
        room.available_rooms -= quantity
        db.commit()
        db.refresh(room)
        return room
    return None

def delete_room(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room:
        db.delete(room)
        db.commit()
        return {"message": "Habitación eliminada correctamente"}
    return {"error": "Habitación no encontrada"}

# --- RESERVATION FUNCTIONS ---
def create_reservation(db: Session, user_id: int, room_id: int, start_date, end_date, quantity: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not room or not user or room.available_rooms < quantity:
        return None
    total_price = calculate_total_price(room.price_per_night, quantity, start_date, end_date)
    reservation = Reservation(user_id=user_id, room_id=room_id, start_date=start_date, end_date=end_date, quantity=quantity, total_price=total_price)
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    room.available_rooms -= quantity
    db.commit()
    return reservation

def get_reservations(db: Session, user_id: int = None, skip: int = 0, limit: int = 10):
    query = db.query(Reservation)
    if user_id:
        query = query.filter(Reservation.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def get_reservation(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def update_reservation(db: Session, reservation_id: int, start_date: datetime, end_date: datetime, quantity: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return None
    
    room = db.query(Room).filter(Room.id == reservation.room_id).first()
    if not room:
        return None

    if room.available_rooms + reservation.quantity < quantity:
        return None

    room.available_rooms += reservation.quantity  # Restore previous room availability
    total_price = calculate_total_price(room.price_per_night, quantity, start_date, end_date)
    
    reservation.start_date = start_date
    reservation.end_date = end_date
    reservation.quantity = quantity
    reservation.total_price = total_price
    
    room.available_rooms -= quantity  # Deduct new reservation quantity
    db.commit()
    db.refresh(reservation)
    return reservation

def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return {"error": "Reserva no encontrada"}

    room = db.query(Room).filter(Room.id == reservation.room_id).first()
    if room:
        room.available_rooms += reservation.quantity  # Restaurar habitaciones disponibles
    
    db.delete(reservation)
    db.commit()
    return {"message": "Reserva eliminada correctamente"}

def is_room_available(db: Session, room_id: int, check_in: datetime, check_out: datetime) -> bool:
    return not db.query(Reservation).filter(
        Reservation.room_id == room_id,
        and_(Reservation.start_date < check_out, Reservation.end_date > check_in)
    ).first()

# --- MATCH FUNCTIONS ---
def get_matches(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Match).offset(skip).limit(limit).all()

def get_match(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()

def create_match(db: Session, match: MatchCreate):
    db_match = Match(
        competition_id=match.competition_id,
        player1_id=match.player1_id,
        player2_id=match.player2_id,
        player1_score=0,
        player2_score=0,
        round_number=1
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def update_match_score(db: Session, match_id: int, score_update: MatchUpdateScore):
    match = db.query(Match).filter(Match.id == match_id).first()
    if match:
        match.player1_score = score_update.player1_score
        match.player2_score = score_update.player2_score
        db.commit()
        db.refresh(match)
    return match

def delete_match(db: Session, match_id: int):
    match = db.query(Match).filter(Match.id == match_id).first()
    if match:
        db.delete(match)
        db.commit()
        return {"message": "Partido eliminado correctamente"}
    return {"error": "Partido no encontrado"}

# --- ADVANCE ROUND FUNCTION ---
def advance_round(db: Session, match_id: int, winner_id: int):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return None
    
    next_round_number = match.round_number + 1

    next_match = db.query(Match).filter(
        Match.competition_id == match.competition_id,
        Match.round_number == next_round_number
    ).first()

    if next_match:
        if not next_match.player1_id:
            next_match.player1_id = winner_id
        elif not next_match.player2_id:
            next_match.player2_id = winner_id
        else:
            return None
    else:
        next_match = Match(
            competition_id=match.competition_id,
            player1_id=winner_id,
            player2_id=None,
            player1_score=0,
            player2_score=0,
            round_number=next_round_number
        )
        db.add(next_match)

    db.commit()
    db.refresh(next_match)
    return next_match
