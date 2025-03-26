from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_matches, get_match, create_match, update_match_score, advance_round, delete_match
from app.schemas.match import MatchCreate, MatchUpdateScore  # Assegura't que aquests esquemes existeixen

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/")
def list_matches(db: Session = Depends(get_db)):
    return get_matches(db)

@router.get("/{match_id}")
def read_match(match_id: int, db: Session = Depends(get_db)):
    match = get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partit no encontrado")
    return match

@router.post("/")
def create_match_route(match: MatchCreate, db: Session = Depends(get_db)):
    return create_match(db, match)

@router.put("/{match_id}/score")
def update_match_score_route(match_id: int, score_data: MatchUpdateScore, db: Session = Depends(get_db)):
    match = update_match_score(db, match_id, score_data.dict())
    if not match:
        raise HTTPException(status_code=404, detail="Partit no encontrado")
    return match

@router.put("/{match_id}/advance")
def advance_round_route(match_id: int, db: Session = Depends(get_db)):
    match = advance_round(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partit no encontrado")
    return match

@router.delete("/{match_id}")
def delete_match_route(match_id: int, db: Session = Depends(get_db)):
    match = delete_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partit no encontrado")
    return {"message": "Partit eliminado correctamente"}
