# app/models/__init__.py
from .competition import Competition
from .match import Match
from .registration import Registration
from .reservation import Reservation
from .room import Room
from .score import Score
from .team import Team
from .user import User

from app.database import Base  # Importa la clase Base si la tienes

__all__ = [
    "Base", 
    "Competition", "Match", "Registration", "Reservation", "Room", "Score", "Team", "User"
]
