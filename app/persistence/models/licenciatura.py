from sqlalchemy import Column, Integer, String, ForeignKey
from app.infrastructure.database import Base


class Licenciatura(Base):
    __tablename__ = 'licenciatura'
    idLicenciatura = Column(Integer, primary_key=True, autoincrement=True)
    nombreLic = Column(String(50), nullable=False, unique=True)

    nivelId = Column(Integer, ForeignKey(
        'nivelAcademico.idNivel'), nullable=False)

    def __repr__(self):
        return f"<Licenciatura(idLicenciatura={self.idLicenciatura}, nombreLic='{self.nombreLic}', nivelId={self.nivelId})>"
