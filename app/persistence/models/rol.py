from sqlalchemy import Column, Integer, String
from app.infrastructure.database import Base


class Rol(Base):
    __tablename__ = 'rol'

    idRol = Column(Integer, primary_key=True, autoincrement=True)
    nombreRol = Column(String(8), nullable=False, unique=True)

    def __repr__(self):
        return f"<Rol(idRol={self.idRol}, nombreRol='{self.nombreRol}')>"
