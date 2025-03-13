from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReservationBase(BaseModel):
    check_in: date
    check_out: date

    class Config:
        from_attributes = True

class ReservationCreate(ReservationBase):
    user_id: int
    competition_id: Optional[int] = None

class ReservationRead(ReservationBase):
    id: int
    user_id: int
    competition_id: Optional[int] = None

    class Config:
        from_attributes = True

class ReservationUpdate(BaseModel):
    check_in: Optional[date] = None
    check_out: Optional[date] = None

    class Config:
        from_attributes = True
