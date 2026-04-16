from sqlalchemy import Column, Integer, String, Date, Time
from app.infrastructure.database import Base


class Noticia(Base):
    __tablename__ = 'noticias'

    idNoticia = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=False)
    # 0: Borrada, 1: Piblicada
    estado = Column(Integer, nullable=False, default=1)
    fechaPublicacion = Column(Date, nullable=False)
    horaPublicacion = Column(Time, nullable=False)

    def __repr__(self):
        return f"<Noticia(idNoticia={self.idNoticia}, titulo='{self.titulo}', estado={self.estado})>"
