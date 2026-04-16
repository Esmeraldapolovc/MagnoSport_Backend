from abc import ABC, abstractmethod
from app.domain.entities import Licenciatura
from ...dtos.usuario.alumnoCreateDTO import AlumnoCreateDTO


class ILicenciaturaService(ABC):
    @abstractmethod
    def obtenerLicenciatura(self) -> list[Licenciatura]:
        pass