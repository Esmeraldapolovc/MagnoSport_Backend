from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any

from pendulum import date
from app.domain.entities.usuario import Usuario



class IAsistenciasyReservasService(ABC):
    @abstractmethod
    def obtenerHorariosAsistenciasyReservas(self, idArea: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def obtenerHorariosAsistenciasyReservasPorFecha(self, fecha_referencia: date, idArea: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def detallesUsuarioReserva(self, idReserva: int) -> dict:
        pass

    @abstractmethod
    def registrarAsistencia(self, idReserva: int) -> dict:
        pass