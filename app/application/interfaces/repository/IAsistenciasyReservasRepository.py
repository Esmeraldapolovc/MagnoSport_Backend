from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Reserva


class IAsistenciasyReservasRepository(ABC):
    @abstractmethod
    def obtenerHorariosAsistenciasyReservas(self, idArea: int):
        pass

    @abstractmethod
    def detallesUsuarioReserva(self, idReserva: int)  -> Reserva:
        pass

    @abstractmethod
    def registrarAsistencia(self, idReserva: int) -> bool:
        pass

    @abstractmethod
    def obtenerReservaPorId(self, idReserva: int) -> Optional[Reserva]:
        pass