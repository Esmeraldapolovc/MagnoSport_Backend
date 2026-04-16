from typing import Optional
from datetime import time
from enum import Enum
from .reserva import Reserva
from .equipo import Equipo

# Enum


class EstadoUso(Enum):
    PENDIENTE = 'Pendiente'
    EN_USO = "En Uso"
    FIN_USO = "Fin Uso"


class ReservaEquipo:
    def __init__(
            self,
            reserva: Reserva,
            equipo: Equipo,
            idReservaEquipo: Optional[int] = None,
            horaInicio: Optional[time] = None,
            horaFin: Optional[time] = None,
            estadoUso: Optional [EstadoUso] = None,
    ):
        self.idReservaEquipo = idReservaEquipo
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.estadoUso = estadoUso
        self.reserva = reserva
        self.equipo = equipo

 

     
     