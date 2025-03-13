from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Registration(Base):
    __tablename__ = 'registrations'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    competition_id = Column(Integer, ForeignKey('competitions.id'))

    # Relacionar el usuario con la competición
    user = relationship("User", back_populates="registrations")
    competition = relationship("Competition", back_populates="registrations")

    def __repr__(self):
        return f"<Registration(id={self.id}, user_id={self.user_id}, competition_id={self.competition_id})>"

    def set_user_as_player(self):
        """Actualizar el estado del usuario a jugador cuando se registre en una competición"""
        if not self.user.is_player:  # Solo cambiamos a jugador si no lo es ya
            self.user.is_player = True
