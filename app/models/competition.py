from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum

class CompetitionType(PyEnum):
    INDIVIDUAL = "individual"
    TEAM = "team"

class Competition(Base):
    __tablename__ = 'competitions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    max_participants = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    competition_type = Column(Enum(CompetitionType), nullable=False) 
    age_restriction = Column(Integer, nullable=True) 
    gender_restriction = Column(String, nullable=True) 

    registrations = relationship("Registration", back_populates="competition", cascade="all, delete-orphan")
    teams = relationship("Team", back_populates="competition", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('max_participants > 0', name='check_max_participants_positive'),
        CheckConstraint('start_date < end_date', name='check_valid_dates'),
    )

    def __repr__(self):
        return f"<Competition(id={self.id}, name={self.name}, max_participants={self.max_participants})>"
