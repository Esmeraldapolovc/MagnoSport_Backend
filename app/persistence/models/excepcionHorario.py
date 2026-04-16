from sqlalchemy import Column, Integer, Date, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from app.persistence.models.enums import EstadoExcepcion


class ExcepcionHorario(Base):
    __tablename__ = 'excepcionHorario'
    idExcepcion = Column(Integer, primary_key=True, autoincrement=True)
    fechaInicio = Column(Date, nullable=False)
    fechaFin = Column(Date, nullable=False)
    horaInicio = Column(Time, nullable=False)
    horaFin = Column(Time, nullable=False)
    estado = Column(Enum(EstadoExcepcion, values_callable=lambda obj: [e.value for e in obj]), nullable=False)

    horarioId = Column(Integer, ForeignKey(
        'horario.idHorario'), nullable=False)

    horario = relationship("Horario", back_populates="excepciones")
    def __repr__(self):
        return f"<ExcepcionHorario(idExcepcion={self.idExcepcion}, fechaInicio={self.fechaInicio}, fechaFin={self.fechaFin}, horaInicio={self.horaInicio}, horaFin={self.horaFin}, estado='{self.estado.value}', horarioId={self.horarioId})>"
