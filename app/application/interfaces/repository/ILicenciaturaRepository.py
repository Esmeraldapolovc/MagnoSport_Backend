from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities import Licenciatura

class ILicenciaturaRepository(ABC):
    @abstractmethod
    def obtenerLicenciatura(self, lic: Licenciatura) -> Licenciatura:
        pass

    @abstractmethod
    def listarLicenciaturas(self) -> list[Licenciatura]:
        pass
