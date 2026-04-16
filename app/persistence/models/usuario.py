from sqlalchemy import Column, Integer, String, ForeignKey
from app.infrastructure.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = 'usuario'
    idUsuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    correo = Column(String(70), nullable=False, unique=True)
    foto = Column(String(255), nullable=True)
    contrasenia = Column(String(255), nullable=False)
    # 1: activo, 0: inactivo
    estatus = Column(Integer, nullable=False, default=1)

    rolId = Column(Integer, ForeignKey('rol.idRol'), nullable=False)
    alumno = relationship("Alumno", backref="usuario_base", uselist=False)
    rol = relationship("Rol")
    def __repr__(self):
        return f"<Usuario(idUsuario={self.idUsuario}, nombre='{self.nombre}', correo='{self.correo}', rolId={self.rolId})>"
