from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud import get_user, get_users, create_user, update_user, delete_user  

router = APIRouter(prefix="/users", tags=["users"])

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para listar todos los usuarios
@router.get("/", response_model=List[UserRead], tags=["users"])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

# Endpoint para obtener detalles de un usuario específico por su ID
@router.get("/{user_id}", response_model=UserRead, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

# Endpoint para crear un nuevo usuario
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear usuario")
    return db_user

# Endpoint para actualizar el perfil de un usuario existente
@router.put("/{user_id}", response_model=UserRead, tags=["users"])
def update_user_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return update_user(db, user_id=user_id, user_update=user_update)

# Endpoint para eliminar una cuenta de usuario
@router.delete("/{user_id}", response_model=dict, tags=["users"], operation_id="delete_user_account_unique")
def delete_user_account(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    delete_user(db, user_id=user_id)
    return {"detail": "Usuario eliminado correctamente"}
