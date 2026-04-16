from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Date
from app.infrastructure.database import Base
from .enums import CategoriaEquipo, EstadoEquipo


class Equipo(Base):
    __tablename__ = 'equipo'

    idEquipo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(90), nullable=False)
    cantidad = Column(Integer, nullable=False)
    categoria = Column(Enum(CategoriaEquipo, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    fechaRegistro = Column(Date, nullable=False)
    estado = Column(Enum(EstadoEquipo, values_callable=lambda obj: [e.value for e in obj]), nullable=False)

    areaId = Column(Integer, ForeignKey('area.idArea'), nullable=False)

    def __repr__(self):
        return f"<Equipo(idEquipo={self.idEquipo}, nombre='{self.nombre}', cantidad={self.cantidad}, categoria='{self.categoria.value}', fechaRegistro={self.fechaRegistro}, estado='{self.estado.value}', areaId={self.areaId})>"
