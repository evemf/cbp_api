from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    
    email = Column(String, unique=True, index=True, nullable=False)  

    first_name = Column(String, index=True, nullable=False)  
    last_name = Column(String, index=True, nullable=False)
    gender = Column(String, nullable=False)
    country = Column(String, index=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True) 

    is_admin = Column(Boolean, default=False)
    is_player = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False) 
    is_profile_complete = Column(Boolean, default=False) 

    verification_token = Column(String, unique=True, nullable=True)  

    birth_date = Column(Date, nullable=True)

    scores = relationship("Score", back_populates="player")
    registrations = relationship("Registration", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, verified={self.is_verified}, profile_complete={self.is_profile_complete})>"