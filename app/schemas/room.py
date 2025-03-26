from pydantic import BaseModel
from typing import Optional

class RoomCreate(BaseModel):
    room_type: str
    price_per_night: float
    total_rooms: int  

    class Config:
        from_attributes = True

class RoomRead(BaseModel):
    id: int
    room_type: str
    price_per_night: float
    total_rooms: int
    available_rooms: int 

    class Config:
        from_attributes = True

class RoomUpdate(BaseModel):
    room_type: Optional[str] = None
    price_per_night: Optional[float] = None
    total_rooms: Optional[int] = None
    available_rooms: Optional[int] = None

    class Config:
        from_attributes = True
