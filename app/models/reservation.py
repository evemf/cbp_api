from sqlalchemy import Column, Integer, ForeignKey, Date, Float
from app.database import Base
from sqlalchemy.orm import relationship

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    total_price = Column(Float)
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation(id={self.id}, user_id={self.user_id}, room_id={self.room_id}, total_price={self.total_price})>"
