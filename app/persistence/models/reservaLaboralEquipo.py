from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Time
from app.infrastructure.database import Base
from .enums import EstadoUsoEquipo


class ReservaLaboralEquipo(Base):
    __tablename__ = 'reservaLaboralEquipo'

    idRLE = Column(Integer, primary_key=True, autoincrement=True)

    cantidad = Column(Integer, nullable=True)
    estadoUso = Column(Enum(EstadoUsoEquipo), nullable=False)
    horaInicio = Column(Time, nullable=False)
    horaFin = Column(Time, nullable=False)

    reservaId = Column(Integer, ForeignKey(
        'reservaLaboral.idReserva'), nullable=False)
    equipoId = Column(Integer, ForeignKey('equipo.idEquipo'), nullable=False)

    def __repr__(self):
        return f"<ReservaLaboralEquipo(idRLE={self.idRLE}, cantidad={self.cantidad}, estadoUso='{self.estadoUso.value}', horaInicio={self.horaInicio}, horaFin={self.horaFin}, reservaId={self.reservaId}, equipoId={self.equipoId})>"
