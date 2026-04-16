from sqlalchemy import Column, Integer, String
from app.infrastructure.database import Base


class NivelAcademico(Base):
    __tablename__ = 'nivelAcademico'

    idNivel = Column(Integer, primary_key=True, autoincrement=True)
    nombreNivel = Column(String(12), nullable=False, unique=True)

    def __repr__(self):
        return f"<NivelAcademico(idNivel={self.idNivel}, nombreNivel='{self.nombreNivel}')>"
