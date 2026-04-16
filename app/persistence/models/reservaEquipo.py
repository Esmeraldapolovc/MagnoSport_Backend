from sqlalchemy import Column, Integer, String, Time, Enum, ForeignKey
from app.infrastructure.database import Base
from .enums import EstadoUsoEquipo
from sqlalchemy.orm import relationship

class ReservaEquipo(Base):
    __tablename__ = 'reservaEquipo'

    idReservaEquipo = Column(Integer, primary_key=True, autoincrement=True)
    horaInicio = Column(Time, nullable=True)
    horaFin = Column(Time, nullable=True)
    estadoUso = Column(Enum(EstadoUsoEquipo, values_callable=lambda obj: [e.value for e in obj]), nullable=False)

    reservaId = Column(Integer, ForeignKey(
        'reserva.idReserva'), nullable=False)
    equipoId = Column(Integer, ForeignKey('equipo.idEquipo'), nullable=False)

    equipo = relationship("Equipo")
    reserva = relationship("Reserva")
    def __repr__(self):
        return f"<ReservaEquipo(idReservaEquipo={self.idReservaEquipo}, horaInicio={self.horaInicio}, horaFin={self.horaFin}, estadoUso='{self.estadoUso.value}', reservaId={self.reservaId}, equipoId={self.equipoId})>"
