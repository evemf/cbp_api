from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCompleteProfile, UserUpdate
from app.utils.security import hash_password, create_verification_token, verify_password
from sqlalchemy.orm import Session
from app.models.match import Match
from app.schemas.match import MatchCreate, MatchUpdateScore
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from app.models.room import Room

# 🔹 Obtener usuario por email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# 🔹 Obtener usuario por ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# 🔹 Obtener lista de usuarios
def get_users(db: Session):
    return db.query(User).all()

# 🔹 Crear usuario con solo email (registro)
def create_user(db: Session, email: str):
    temp_password = hash_password("temporary")  # Contraseña temporal
    verification_token = create_verification_token(email)  # 🔹 Generar token
    new_user = User(email=email, hashed_password=temp_password, verification_token=verification_token)  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 🔹 Completar perfil de usuario
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

def authenticate_user(db: Session, email: str, password: str):
    print(f"🔍 Buscando usuario con email: {email}")

    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    
    if not user:
        print("❌ Usuario no encontrado o inactivo")
        return None

    print(f"✅ Usuario encontrado: {user.email}")
    print(f"🔍 Hash en la BD: {user.hashed_password}")
    print(f"🔍 Comparando con la contraseña ingresada: {password}")

    if not verify_password(password, user.hashed_password):
        print("❌ Contraseña incorrecta")
        return None

    print("✅ Autenticación exitosa")
    return user



# 🔹 Actualizar perfil (sin modificar email)
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = get_user(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado.")

    if user_update.password:
        user.hashed_password = hash_password(user_update.password)

    if user_update.birth_date:
        user.birth_date = user_update.birth_date
    if user_update.gender:
        user.gender = user_update.gender
    if user_update.country:
        user.country = user_update.country
    if user_update.phone_number:
        user.phone_number = user_update.phone_number

    db.commit()
    db.refresh(user)
    return user

# 🔹 Eliminar usuario
def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado.")

    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado correctamente."}


def get_matches(db: Session):
    """Obtiene todos los partidos"""
    return db.query(Match).all()

def get_match(db: Session, match_id: int):
    """Obtiene un partido por su ID"""
    return db.query(Match).filter(Match.id == match_id).first()

def create_match(db: Session, match_data: MatchCreate):
    """Crea un nuevo partido"""
    match = Match(
        competition_id=match_data.competition_id,
        player1_id=match_data.player1_id,
        player2_id=match_data.player2_id,
        score_player1=0,
        score_player2=0,
        winner_id=None
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

def update_match_score(db: Session, match_id: int, score_data: MatchUpdateScore):
    """Actualiza el puntaje de un partido"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return None
    match.score_player1 = score_data.player1_score
    match.score_player2 = score_data.player2_score
    if match.score_player1 == 5 or match.score_player2 == 5:
        match.winner_id = match.player1_id if match.score_player1 == 5 else match.player2_id
    db.commit()
    db.refresh(match)
    return match

def advance_round(db: Session, match_id: int, winner_id: int):
    """Avanza al jugador ganador a la siguiente ronda"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match or not match.winner_id:
        return None
    # Aquí deberías definir cómo se asigna al ganador al siguiente match
    return {"message": "Avanzado a la siguiente ronda"}

def delete_match(db: Session, match_id: int):
    """Elimina un partido"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return False
    db.delete(match)
    db.commit()
    return True

def create_reservation(db: Session, reservation_data: ReservationCreate):
    """Crea una nueva reserva en la base de datos"""
    reservation = Reservation(
        user_id=reservation_data.user_id,
        date=reservation_data.date,
        time=reservation_data.time,
        court_id=reservation_data.court_id
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def get_reservations(db: Session):
    """Obtiene todas las reservas en la base de datos"""
    return db.query(Reservation).all()

def get_reservation(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

# Crear una reserva
def create_reservation(db: Session, reservation_data):
    new_reservation = Reservation(**reservation_data.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

# Actualizar una reserva
def update_reservation(db: Session, reservation_id: int, update_data):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return None
    for key, value in update_data.dict().items():
        setattr(reservation, key, value)
    db.commit()
    db.refresh(reservation)
    return reservation

# Eliminar una reserva
def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return None
    db.delete(reservation)
    db.commit()
    return True

# Verificar disponibilidad de una sala
def is_room_available(db: Session, room_id: int, start_time, end_time):
    overlapping_reservations = db.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).all()
    return len(overlapping_reservations) == 0

# Crear una nueva sala
def create_room(db: Session, room_data):
    new_room = Room(**room_data.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

# Obtener una sala por ID
def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

# Obtener todas las salas
def get_rooms(db: Session):
    return db.query(Room).all()

# Eliminar una sala
def delete_room(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None
    db.delete(room)
    db.commit()
    return True

# Actualizar disponibilidad de salas
def update_available_rooms(db: Session):
    # Lógica para actualizar salas disponibles
    pass  # Implementar según la lógica del negocio