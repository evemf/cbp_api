from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from .base import UserCreate, UserRead, UserUpdate
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}", response_model=UserRead, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    from app.crud import get_user
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

@router.get("/", response_model=list[UserRead], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    from app.crud import get_users
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=UserRead, tags=["users"])
def create_user_profile(user: UserCreate, db: Session = Depends(get_db)):
    from app.crud import create_user
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Correo electrónico ya registrado")
    new_user = create_user(db, user=user)
    return new_user

@router.put("/{user_id}", response_model=UserRead, tags=["users"])
def update_user_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    from app.crud import update_user
    user = update_user(db, user_id=user_id, user_update=user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

@router.delete("/{user_id}", response_model=UserRead, tags=["users"])
def delete_user_profile(user_id: int, db: Session = Depends(get_db)):
    from app.crud import delete_user
    user = delete_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user
