from fastapi import APIRouter, HTTPException, Request, Depends, Cookie, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRead, UserCompleteProfile, UserUpdate
from app.crud import get_user_by_email, complete_user_profile, update_user, delete_user, get_user, get_users
from app.utils.security import create_access_token
from app.utils.token_utils import verify_verification_token

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/complete-profile", response_model=UserRead)
async def complete_profile(profile_data: UserCompleteProfile, request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("verification_token")
    if not token:
        raise HTTPException(status_code=400, detail="Token de verificación no proporcionado.")
    try:
        email = verify_verification_token(token)
    except Exception:
        raise HTTPException(status_code=400, detail="Token no válido o expirado.")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if user.is_profile_complete:
        raise HTTPException(status_code=400, detail="El perfil ya ha sido completado.")
    user = complete_user_profile(db, user, profile_data)
    # Generar l'access_token per a que l'usuari ja estigui autenticat
    token_data = {"sub": user.email, "type": "access"}
    access_token = create_access_token(data=token_data)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=3600,
        path="/"
    )
    response.delete_cookie("verification_token")
    return UserRead.from_orm(user)


@router.get("/profile", response_model=UserRead)
def get_user_profile(request: Request, db: Session = Depends(get_db), access_token: str | None = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="No autenticado")
    try:
        email = verify_verification_token(access_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserRead.from_orm(user)

@router.put("/{user_id}", response_model=UserRead)
def update_user_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    updated_user = update_user(db, user_id, user_update.dict(exclude_unset=True))
    return updated_user

@router.delete("/{user_id}", response_model=dict)
def delete_user_account(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return delete_user(db, user_id)


