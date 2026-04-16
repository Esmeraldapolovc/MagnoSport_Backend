from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Horario, ExcepcionHorario
from datetime import date

class IHorarioRepository(ABC):
    
    @abstractmethod
    def crearHorario(self, horario: Horario, diasIds: List[int]) -> Horario:
        pass

    @abstractmethod
    def listarHorarios(self) -> List[Horario]:
        pass

    @abstractmethod
    def verificarSolapamiento(self, fechaInicio, fechaFin, horaInicio, horaFin, diasIds: List[int]) -> bool:
        
        pass

    @abstractmethod
    def crearExcepcion(self, excepcion: ExcepcionHorario) -> ExcepcionHorario:
        pass

    @abstractmethod
    def obtenerPorId(self, id: int) -> Horario:
     pass

    @abstractmethod
    def buscarPorFecha(self, fecha: date) -> Optional[Horario]:
        pass
    

    @abstractmethod
    def obtenerExcepcionesPorHorario(self, horario_id: int) -> List[ExcepcionHorario]:
        pass
