from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReservationBase(BaseModel):
    check_in: date
    check_out: date

    class Config:
        from_attributes = True  # Para Pydantic v2 (en v1 usar orm_mode = True)

class ReservationCreate(ReservationBase):
    user_id: int
    competition_id: Optional[int] = None

    class Config:
        from_attributes = True  # Para coherencia con los otros esquemas

class ReservationRead(ReservationBase):
    id: int
    user_id: int
    competition_id: Optional[int] = None

    class Config:
        from_attributes = True

class ReservationUpdate(ReservationBase):
    check_in: Optional[date] = None
    check_out: Optional[date] = None
