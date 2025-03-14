from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    birth_date = Column(Date)
    gender = Column(String)
    email = Column(String, unique=True, index=True)
    country = Column(String, index=True)
    phone_number = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_player = Column(Boolean, default=False)  
    is_active = Column(Boolean, default=False) 
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, unique=True, nullable=True) 
    is_profile_complete = Column(Boolean, default=False)

    scores = relationship("Score", back_populates="player")
    registrations = relationship("Registration", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")  

    def __repr__(self):
        return f"<User(id={self.id}, name={self.first_name} {self.last_name}, email={self.email}, is_player={self.is_player})>"
