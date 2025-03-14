from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserVerify, UserCompleteProfile as UserComplete
from app.crud import (
    get_user, get_users, create_user, update_user, delete_user, 
    verify_email, complete_user_profile, get_user_by_email
)
from app.utils.email_utils import send_verification_email

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

@router.put("/complete-profile", response_model=UserRead)
def complete_profile(data: UserComplete, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    updated_user = complete_user_profile(db, user.id, data)
    print("Usuario actualizado:", updated_user)
    if not updated_user: 
        raise HTTPException(status_code=500, detail="Error al actualizar el perfil")

    return updated_user

@router.put("/{user_id}", response_model=UserRead)
def update_user_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    updated_user = update_user(db, user_id=user_id, user_update=user_update)
    return updated_user

@router.delete("/{user_id}", response_model=dict)
def delete_user_account(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    response = delete_user(db, user_id=user_id) 
    return response  

