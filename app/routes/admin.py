from fastapi import APIRouter, HTTPException, Request, Header, Depends, Cookie, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserRead
from app.crud import update_user as update_user_crud
from app.utils.security import verify_access_token

router = APIRouter(prefix="/admin", tags=["admin"])

def is_admin(user: User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")

@router.get("/users")
def get_users_route(
    request: Request, 
    db: Session = Depends(get_db), 
    authorization: str = Header(None)
):
    access_token = request.cookies.get("access_token")
    print("TOKEN REBUT EN COOKIES:", access_token)
    if not access_token and authorization:
        access_token = authorization.replace("Bearer ", "")
    if not access_token:
        raise HTTPException(status_code=401, detail="No autenticado")
    try:
        email = verify_access_token(access_token)
        print("EMAIL DESDEL TOKEN:", email)
        user = db.query(User).filter(User.email == email).first()
        print("Usuari recuperat:", user)
        is_admin(user)
        return db.query(User).all()
    except Exception as e:
        print("ERROR durant la verificació del token:", e)
        raise HTTPException(status_code=401, detail=f"Token inválido o expirado: {str(e)}")


@router.put("/admin/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user_crud(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    return {"message": "Usuario actualizado correctamente", "user": updated_user}

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int, 
    request: Request, 
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    # Obtener token desde cookies o headers
    access_token = request.cookies.get("access_token")
    if not access_token and authorization:
        access_token = authorization.replace("Bearer ", "")
    if not access_token:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    # Verificar usuario
    try:
        email = verify_access_token(access_token)
        user = db.query(User).filter(User.email == email).first()
        is_admin(user)  # Verifica que el usuario es admin
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido o expirado: {str(e)}")

    # Buscar usuario a eliminar
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user_to_delete)
    db.commit()

    return {"message": f"Usuario {user_id} eliminado correctamente"}