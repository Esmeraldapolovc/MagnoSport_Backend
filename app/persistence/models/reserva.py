from sqlalchemy import Column, Integer, Date, Time, Enum, ForeignKey
from app.infrastructure.database import Base
from .enums import EstadoReserva, tipoReserva, MotivoCancelacion
from sqlalchemy.orm import relationship

class Reserva(Base):
    __tablename__ = 'reserva'

    idReserva = Column(Integer, primary_key=True, autoincrement=True)
    fechaReserva = Column(Date, nullable=False)
    horaInicio = Column(Time, nullable=False)
    horaFin = Column(Time, nullable=False)
    motivoCancelacion = Column(Enum(MotivoCancelacion, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    estado = Column(Enum(EstadoReserva, values_callable=lambda obj: [e.value for e in obj]), nullable=True)
    tipoReserva = Column(Enum(tipoReserva, values_callable=lambda obj: [e.value for e in obj]), nullable=True)

    areaId = Column(Integer, ForeignKey('area.idArea'), nullable=False)
    usuarioId = Column(Integer, ForeignKey(
        'usuario.idUsuario'), nullable=False)
    horarioId = Column(Integer, ForeignKey(
        'horario.idHorario'), nullable=False)
    
    horario = relationship("Horario", back_populates="reservas")
    usuario = relationship("Usuario") 
    area = relationship("Area")
    reserva_equipos = relationship("ReservaEquipo", backref="reserva_principal")
    reserva_laboral = relationship("ReservaLaboral", uselist=False, back_populates="reserva_base")
    def __repr__(self):
        return f"<Reserva(idReserva={self.idReserva}, fechaReserva={self.fechaReserva}, horaInicio={self.horaInicio}, horaFin={self.horaFin}, motivoCancelacion='{self.motivoCancelacion.value if self.motivoCancelacion else None}', estado='{self.estado.value}', tipo='{self.tipoReserva}', areaId={self.areaId}, usuarioId={self.usuarioId}, horarioId={self.horarioId})>"
