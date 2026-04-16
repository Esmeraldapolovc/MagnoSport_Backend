from sqlalchemy import Column, Integer, String
from app.infrastructure.database import Base


class Area(Base):
    __tablename__ = 'area'

    idArea = Column(Integer, primary_key=True, autoincrement=True)
    nombreArea = Column(String(25), nullable=False, unique=True)

    def __repr__(self):
        return f"<Area(idArea={self.idArea}, nombreArea='{self.nombreArea}')>"
