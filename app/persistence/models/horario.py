from sqlalchemy import Column, Integer, Date, Time, Enum
from app.infrastructure.database import Base
from sqlalchemy.orm import relationship
from app.persistence.models.enums import EstadoHorario


class Horario(Base):
    __tablename__ = 'horario'

    idHorario = Column(Integer, primary_key=True, autoincrement=True)
    fechaInicio = Column(Date, nullable=False)
    fechaFin = Column(Date, nullable=False)
    horaInicio = Column(Time, nullable=False)
    horaFin = Column(Time, nullable=False)
    estado = Column(Enum(EstadoHorario, values_callable=lambda obj: [e.value for e in obj]), nullable=False)

    dias = relationship("Dia", secondary="horarioDia", backref="horarios")
    reservas = relationship("Reserva", back_populates="horario")
    excepciones = relationship("ExcepcionHorario", back_populates="horario")
    def __repr__(self):
        return f"<Horario(idHorario={self.idHorario}, fechaInicio={self.fechaInicio}, fechaFin={self.fechaFin}, horaInicio={self.horaInicio}, horaFin={self.horaFin}, estado='{self.estado.value}')>"
