from sqlalchemy import Column, Integer, String
from app.infrastructure.database import Base


class Dia(Base):
    __tablename__ = 'dia'

    idDia = Column(Integer, primary_key=True, autoincrement=True)
    nombreDia = Column(String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"<Dia(idDia={self.idDia}, nombreDia='{self.nombreDia}')>"
