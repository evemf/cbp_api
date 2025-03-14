from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    room_type = Column(String)  
    price_per_night = Column(Float)  
    total_rooms = Column(Integer, default=0)  
    available_rooms = Column(Integer, default=0)  
    available = Column(Boolean, default=True) 
    reservations = relationship("Reservation", back_populates="room")
    
    def __repr__(self):
        return f"<Room(id={self.id}, room_type={self.room_type}, price_per_night={self.price_per_night}, total_rooms={self.total_rooms}, available_rooms={self.available_rooms})>"

