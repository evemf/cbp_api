from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CompetitionBase(BaseModel):
    name: str
    description: Optional[str] = None
    max_participants: int
    is_active: bool = True
    start_date: datetime
    end_date: datetime
    competition_type: str
    age_restriction: Optional[int] = None
    gender_restriction: Optional[str] = None

    class Config:
        from_attributes = True

class CompetitionCreate(CompetitionBase):
    pass

class CompetitionRead(CompetitionBase):
    id: int

    class Config:
        from_attributes = True

class CompetitionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_participants: Optional[int] = None
    is_active: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    competition_type: Optional[str] = None
    age_restriction: Optional[int] = None
    gender_restriction: Optional[str] = None

    class Config:
        from_attributes = True
