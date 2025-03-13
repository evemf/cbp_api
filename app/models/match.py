from sqlalchemy import Column, Integer, ForeignKey, String, Float
from app.database import Base
from sqlalchemy.orm import relationship

class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, index=True)
    competition_id = Column(Integer, ForeignKey('competitions.id'))
    player1_id = Column(Integer, ForeignKey('users.id'))
    player2_id = Column(Integer, ForeignKey('users.id'))
    score_player1 = Column(Integer)
    score_player2 = Column(Integer)
    winner_id = Column(Integer, ForeignKey('users.id'))

    # Relacionar el match con los scores
    scores = relationship("Score", back_populates="match")
    
    # Relaciones de los jugadores
    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])
    winner = relationship("User", foreign_keys=[winner_id])

    def __repr__(self):
        return f"<Match(id={self.id}, player1={self.player1_id}, player2={self.player2_id}, winner={self.winner_id})>"
