from sqlalchemy import Column, Integer, Date, ForeignKey
from app.infrastructure.database import Base
from sqlalchemy.orm import relationship

class Alumno(Base):
    __tablename__ = 'alumno'

    idUsuario = Column(Integer, ForeignKey(
        'usuario.idUsuario'), primary_key=True)

    fechaInicio = Column(Date, nullable=False)
    fechaFin = Column(Date, nullable=True)

    nivelId = Column(Integer, ForeignKey(
        'nivelAcademico.idNivel'), nullable=False)
    licenciaturaId = Column(Integer, ForeignKey(
        'licenciatura.idLicenciatura'), nullable=True)
    
    nivel = relationship("NivelAcademico") 
    licenciatura = relationship("Licenciatura")