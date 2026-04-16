from abc import ABC, abstractmethod
from app.domain.entities import Rol


class IRolRepository(ABC):
    @abstractmethod
    def obtenerRol(self, rol: Rol) -> Rol:
        pass
