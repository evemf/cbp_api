# app/schemas/__init__.py
from .competition import CompetitionCreate, CompetitionRead
from .reservation import ReservationCreate, ReservationRead
from .match import MatchRead, MatchCreate, MatchUpdateScore
from .base import UserCreate, UserRead, UserUpdate

__all__ = [
    "CompetitionCreate", "CompetitionRead", 
    "ReservationCreate", "ReservationRead",
    "MatchRead", "MatchCreate", "MatchUpdateScore",
    "UserCreate", "UserRead", "UserUpdate",
]
