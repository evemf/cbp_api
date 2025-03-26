from sqlalchemy.orm import Session
from app.schemas.auth import UserRegister
from app.utils.security import hash_password, verify_password
from app.crud import get_user_by_email, create_user as crud_create_user, update_user
from app.models.user import User

def get_users(db: Session):
    return db.query(User).all()

def register_user(db: Session, user_data: UserRegister):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("El email ya está registrado.")
    hashed_password = hash_password(user_data.password)
    return crud_create_user(db, user_data.email, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def verify_user_email(db: Session, email: str):
    user = get_user_by_email(db, email)
    if user and not user.is_verified:
        return update_user(db, user.id, {"is_verified": True})
    return None
