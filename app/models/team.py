from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    competition_id = Column(Integer, ForeignKey('competitions.id'))
    player1_id = Column(Integer, ForeignKey('users.id'))
    player2_id = Column(Integer, ForeignKey('users.id'))

    competition = relationship("Competition", back_populates="teams")
    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])

    def __repr__(self):
        return f"<Team(id={self.id}, player1={self.player1_id}, player2={self.player2_id})>"
