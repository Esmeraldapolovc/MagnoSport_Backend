from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Reserva, ReservaLaboral, ReservaEquipo
from datetime import date, time

class IReservaRepository(ABC):

    @abstractmethod
    def reservaUsuario1(self, reserva: Reserva) -> Reserva:
        
        pass

    @abstractmethod
    def obtenerAgendaRangoUsuario(self, fecha_inicio: date, fecha_fin: date, usuario_id: int) -> List[any]:
        pass

    @abstractmethod
    def reservaLaboral(self, reservalab : ReservaLaboral) -> ReservaLaboral:
        pass

    @abstractmethod
    def reservaCardio(self, reservaCardio: ReservaEquipo) -> ReservaEquipo:
        pass

    @abstractmethod
    def listaReservas(self, fecha: date, hora_inicio: time, hora_fin: time) -> List[any]:
        pass

    @abstractmethod
    def cancelarReserva(self, idReserva: int, usuarioId: int) -> bool:
        pass

    @abstractmethod
    def detalleReserva(self, idReserva: int) -> ReservaEquipo :
        pass

    @abstractmethod
    def buscarMaquinaSustituta(self, nombre_maquina: str, area_id: int, equipo_actual_id: int):
        pass

    @abstractmethod
    def registrarUsoEquipo(self, idReservaEquipo: int) -> ReservaEquipo:
        pass

    @abstractmethod
    def estaEquipoEnUsoPorOtros(self, equipo_id: int, reserva_actual: Reserva) -> bool:

      pass
    
    @abstractmethod
    def actualizarEquipoReserva(self, id_reserva_equipo: int, nuevo_equipo_id: int):
        pass

    @abstractmethod
    def cancelarReservasPorRetraso(self):
        pass

    @abstractmethod
    def agregarEquipoAReserva(self, id_reserva: int, id_equipo: int) -> ReservaEquipo:
        pass

    @abstractmethod
    def obtenerReservaPorId(self, id_reserva: int) -> Optional[Reserva]:
        pass
