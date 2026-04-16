from abc import ABC, abstractmethod
from app.domain.entities import Equipo
class IEquipoRepository(ABC):

    @abstractmethod
    def registrarEquipo(self, equipo: Equipo) -> Equipo:
        pass

    @abstractmethod
    def actualizarEquipo(self, equipo: Equipo) -> Equipo:
        pass


    @abstractmethod
    def ListadoEquipos(self) -> list[Equipo]:
        pass

    @abstractmethod
    def obtenerEquipoPorId(self, idEquipo: int) -> Equipo:
        pass

    @abstractmethod
    def obtenerEquipoPorNombre(self, nombre: str) -> list[Equipo]:
        pass

    @abstractmethod
    def obtenerEquipoGeneralPorNombre (self, nombre: str) -> list[Equipo]:
        pass