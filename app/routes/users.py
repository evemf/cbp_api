from fastapi import APIRouter, HTTPException, Request, Depends, Cookie
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRead, UserCompleteProfile, UserUpdate
from app.crud import get_user_by_email, complete_user_profile, update_user, delete_user, get_user, get_users
from app.utils.security import verify_token, hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/complete-profile", response_model=UserRead)
async def complete_profile(
    profile_data: UserCompleteProfile,
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("verification_token")
    if not token:
        raise HTTPException(status_code=400, detail="Token de verificación no proporcionado.")
    try:
        email = verify_token(token)
    except Exception:
        raise HTTPException(status_code=400, detail="Token no válido o expirado.")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if user.is_profile_complete:
        raise HTTPException(status_code=400, detail="El perfil ya ha sido completado.")
    hashed_password = hash_password(profile_data.password)
    user.first_name = profile_data.first_name
    user.last_name = profile_data.last_name
    user.birth_date = profile_data.birth_date
    user.gender = profile_data.gender
    user.country = profile_data.country
    user.phone_number = profile_data.phone_number
    user.hashed_password = hashed_password
    user.is_profile_complete = True
    db.commit()
    return UserRead.from_orm(user)

@router.get("/profile", response_model=UserRead)
def get_user_profile(
    request: Request,
    db: Session = Depends(get_db),
    access_token: str | None = Cookie(default=None)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="No autenticado")

    try:
        email = verify_token(access_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return UserRead.from_orm(user)


@router.put("/{user_id}", response_model=UserRead)
def update_user_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    updated_user = update_user(db, user_id=user_id, user_update=user_update)
    return updated_user

@router.delete("/{user_id}", response_model=dict)
def delete_user_account(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    response = delete_user(db, user_id=user_id)
    return response
