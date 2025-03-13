from pydantic import BaseModel

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
