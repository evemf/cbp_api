from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.match import MatchRead, MatchCreate, MatchUpdateScore
from app.crud import get_matches, get_match, create_match, update_match_score, advance_round, delete_match


router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/", response_model=list[MatchRead])
def list_matches(db: Session = Depends(get_db)):
    return get_matches(db)

@router.get("/{match_id}", response_model=MatchRead)
def read_match(match_id: int, db: Session = Depends(get_db)):
    match = get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partido no encontrado.")
    return match

@router.post("/", response_model=MatchRead)
def add_match(match: MatchCreate, db: Session = Depends(get_db)):
    return create_match(db, match)

@router.put("/{match_id}/score", response_model=MatchRead)
def update_match_score_route(match_id: int, score: MatchUpdateScore, db: Session = Depends(get_db)):
    match = get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partido no encontrado.")
    if score.player1_score < 0 or score.player2_score < 0:
        raise HTTPException(status_code=400, detail="Los puntajes no pueden ser negativos.")
    updated_match = update_match_score(db, match_id, score)
    if updated_match.player1_score == 5 or updated_match.player2_score == 5:
        winner_id = updated_match.player1_id if updated_match.player1_score == 5 else updated_match.player2_id
        advance_round(db, match_id, winner_id)
    return updated_match

@router.post("/{match_id}/advance")
def advance_match_route(match_id: int, db: Session = Depends(get_db)):
    match = get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partido no encontrado.")
    if match.player1_score < 5 and match.player2_score < 5:
        raise HTTPException(status_code=400, detail="El partido aún no ha finalizado.")
    next_match = advance_round(db, match_id)
    if not next_match:
        raise HTTPException(status_code=400, detail="No se pudo avanzar de ronda.")
    return {"message": "Jugador avanzado a la siguiente ronda", "next_match": next_match}

@router.delete("/{match_id}")
def delete_match_route(match_id: int, db: Session = Depends(get_db)):
    match = get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partido no encontrado.")
    success = delete_match(db, match_id)
    if not success:
        raise HTTPException(status_code=500, detail="No se pudo eliminar el partido.")
    return {"message": "Partido eliminado correctamente"}
