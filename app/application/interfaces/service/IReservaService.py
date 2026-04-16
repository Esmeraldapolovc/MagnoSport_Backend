from abc import ABC, abstractmethod
from app.application.dtos.reserva import ReservaAlumnoCreateDTO, ObtenerAgendaDTO, ReservaDeleteDTO, EstadoUsoUpdateDTO, ReservaDetailsDTO, ReservaEquipoDTO
from typing import Optional, Dict, List, Any
from datetime import date
class IReservaService(ABC):

    @abstractmethod
    def reservaUsuario1(self, dto: ReservaAlumnoCreateDTO) -> str:
        pass
 
    @abstractmethod
    def obtenerAgendaRangoUsuario(self, dto: ObtenerAgendaDTO) ->List[Dict[str, Any]]:
        pass 

    @abstractmethod
    def cancelarReserva(self, dto: ReservaDeleteDTO) -> str:
        pass

    @abstractmethod
    def detalleReserva(self, dto: ReservaDetailsDTO) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def cambiarEstadoEquipo(self, dto: EstadoUsoUpdateDTO) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def buscarHorario(self, fecha: date, dto: ObtenerAgendaDTO) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def agregarEquipoAdicional(self, dto: ReservaEquipoDTO) -> Dict[str, Any]:
        pass


   