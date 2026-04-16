from abc import ABC, abstractmethod
from app.persistence.models.equipo import Equipo
from ...dtos.equipo import AgregarEquipoDTO, ActualizarEquipoDTO

class IEquipoService(ABC):

    @abstractmethod
    def registrarEquipo(self, dto: AgregarEquipoDTO) -> str:
        pass

    @abstractmethod
    def actualizarEquipo(self, dto: ActualizarEquipoDTO) -> str:
        pass

    @abstractmethod
    def ListadoEquipos(self) -> list[Equipo]:
        pass

    
    @abstractmethod
    def obtenerEquipoPorNombre(self, nombre: str) -> list[Equipo]:
        pass

    @abstractmethod
    def obtenerEquipoPorId(self, idEquipo: int) -> Equipo:
        pass

    @abstractmethod
    def obtenerEquipoGeneralPorNombre(self, nombre: str) -> list[Equipo]:
        pass

   