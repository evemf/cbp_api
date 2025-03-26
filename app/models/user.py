from sqlalchemy import Column, Integer, String, Date, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
    player = "player"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    
    email = Column(String, unique=True, index=True, nullable=False)  

    first_name = Column(String, index=True, nullable=True)  # ✅ Ahora es opcional
    last_name = Column(String, index=True, nullable=True)  # ✅ Ahora es opcional
    gender = Column(String, nullable=True)  # ✅ Ahora es opcional
    country = Column(String, index=True, nullable=True)  # ✅ Ahora es opcional
    phone_number = Column(String, unique=True, nullable=True)  # ✅ Ahora es opcional
    hashed_password = Column(String, nullable=True) 

    role = Column(String, nullable=False, default="user")

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False) 
    is_profile_complete = Column(Boolean, default=False) 

    verification_token = Column(String, unique=True, nullable=True)  

    birth_date = Column(Date, nullable=True)

    scores = relationship("Score", back_populates="player")
    registrations = relationship("Registration", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role}, verified={self.is_verified}, profile_complete={self.is_profile_complete})>"