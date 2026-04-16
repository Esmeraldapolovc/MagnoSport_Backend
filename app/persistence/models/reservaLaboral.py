from sqlalchemy import Column, Integer, String, ForeignKey
from app.infrastructure.database import Base
from sqlalchemy.orm import relationship

from app.persistence.models.licenciatura import Licenciatura

class ReservaLaboral(Base):
    __tablename__ = 'reservaLaboral'

    idReserva = Column(Integer, ForeignKey('reserva.idReserva'),
                       primary_key=True, autoincrement=True)
    claseImpartir = Column(String(50), nullable=False)

    licId = Column(Integer, ForeignKey(
        'licenciatura.idLicenciatura'), nullable=False)
    
    licenciatura = relationship("Licenciatura")   
    reserva_base = relationship("Reserva", back_populates="reserva_laboral")
