from abc import ABC, abstractmethod
from app.domain.entities import Rol
from ...dtos.usuario import usuarioCreateDTO


class IRolService(ABC):
    @abstractmethod
    def obtenerRol(self, dto: usuarioCreateDTO) -> Rol:
        pass
