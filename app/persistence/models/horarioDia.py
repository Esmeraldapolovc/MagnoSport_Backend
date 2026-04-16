from sqlalchemy import Column, Integer, ForeignKey
from app.infrastructure.database import Base


class HorarioDia(Base):
    __tablename__ = 'horarioDia'
    idHorarioDia = Column(Integer, primary_key=True, autoincrement=True)
    diaId = Column(Integer, ForeignKey('dia.idDia'), nullable=False)
    horarioId = Column(Integer, ForeignKey(
        'horario.idHorario'), nullable=False)

    def __repr__(self):
        return f"<HorarioDia(idHorarioDia={self.idHorarioDia}, diaId={self.diaId}, horarioId={self.horarioId})>"
