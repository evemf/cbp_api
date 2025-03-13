from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    player_id = Column(Integer, ForeignKey('users.id'))
    points = Column(Integer, default=0)  # Puntos obtenidos en esta partida

    # Relaciones
    match = relationship("Match", back_populates="scores")  # Relación con 'Match'
    player = relationship("User", back_populates="scores")  # Relación con 'User'

    def __repr__(self):
        return f"<Score(id={self.id}, match_id={self.match_id}, player_id={self.player_id}, points={self.points})>"
