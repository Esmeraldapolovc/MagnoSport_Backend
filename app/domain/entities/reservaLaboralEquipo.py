from typing import Optional
from datetime import time
from enum import Enum
from .reserva import Reserva
from .equipo import Equipo
# Enum


class EstadoUso(Enum):
    EN_USO = "En uso"
    FIN_USO = "Fin de uso"


# Entidad
class ReservaLaboralEquipo:
    def __init__(
        self,
        cantidad: int,
        estadoUso: EstadoUso,
        horaInicio: time,
        horaFin: time,
        reserva: Reserva,
        equipo: Equipo,
        idRLE: Optional[int] = None

    ):

        self.idRLE = idRLE
        self.cantidad = cantidad
        self.estadoUso = estadoUso
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.reserva = reserva
        self.equipo = equipo

        if not self.validar_cantidad(cantidad):
            raise ValueError(
                f"La cantidad {cantidad} debe ser un número entero positivo."
            )
        if not self.validar_horas(horaInicio, horaFin):
            raise ValueError(
                f"La hora de inicio {horaInicio} debe ser anterior a la hora de fin {horaFin}."
            )

        if not self.validar_uso_dentro_reserva():
            raise ValueError(
                "El horario de uso del equipo debe estar dentro del horario de la reserva."
            )

        if not self.validar_material_disponible():
            raise ValueError(
                f"La cantidad solicitada de {self.equipo.nombre} excede la cantidad disponible."
            )

    def validar_cantidad(self, cantidad: int) -> bool:
        return cantidad > 0

    def validar_horas(self, horaInicio: time, horaFin: time) -> bool:
        return horaInicio < horaFin

    # verifica que el uso de Material esté dentro del horario de la reserva
    def validar_uso_dentro_reserva(self) -> bool:
        inicio = self.horaInicio >= self.reserva.horaInicio
        fin = self.horaFin <= self.reserva.horaFin
        return inicio and fin

    # valida que la cantidad solicitada de material no exceda la cantidad disponible en el equipo
    def validar_material_disponible(self) -> bool:
        if self.equipo.categoria == "Material":
            return self.cantidad <= self.equipo.cantidad
        return True
