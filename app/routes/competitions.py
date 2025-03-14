from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.competition import Competition  # Agregar app. antes de models
from app.schemas.competition import CompetitionCreate, CompetitionRead, CompetitionUpdate
from app.database import get_db  

router = APIRouter(prefix="/competitions", tags=["competitions"])

@router.get("/", response_model=List[CompetitionRead])
def get_competitions(db: Session = Depends(get_db)):
    return db.query(Competition).all()

@router.get("/{competition_id}", response_model=CompetitionRead)
def get_competition(competition_id: int, db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition

@router.post("/", response_model=CompetitionRead)
def create_competition(comp_data: CompetitionCreate, db: Session = Depends(get_db)):
    new_competition = Competition(**comp_data.dict())
    db.add(new_competition)
    db.commit()
    db.refresh(new_competition)
    return new_competition

@router.put("/{competition_id}", response_model=CompetitionRead)
def update_competition(competition_id: int, comp_update: CompetitionUpdate, db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    
    for key, value in comp_update.dict(exclude_unset=True).items():
        setattr(competition, key, value)

    db.commit()
    db.refresh(competition)
    return competition

@router.patch("/{competition_id}/toggle-active", response_model=CompetitionRead)
def toggle_competition_status(competition_id: int, db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    
    competition.is_active = not competition.is_active
    db.commit()
    db.refresh(competition)
    return competition

@router.delete("/{competition_id}")
def delete_competition(competition_id: int, db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    db.delete(competition)
    db.commit()
    return {"message": "Competition deleted successfully"}
