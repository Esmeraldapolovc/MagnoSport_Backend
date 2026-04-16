from typing import Optional
from datetime import date, time
from enum import Enum
from .area import Area
from .usuario import Usuario
from .horario import Horario
# Enum¿s de reserva


class MotivoCancelacion(Enum):
    CANCELADO_POR_EL_USUARIO = "Cancelado por el usuario"
    CANCELADO_POR_RETRASO = "Cancelado por retraso"


class Estado(Enum):
    PENDIENTE = "Pendiente"
    ASISTIO = "Asistió"
    CANCELADA = "Cancelada"


class TipoReserva(Enum):
    LABORAL = "Laboral"
    PERSONAL = "Personal"


class Reserva:

    def __init__(
            self,
            fechaReserva: date,
            horaInicio: time,
            horaFin: time,
            area: Area,
            usuario: Usuario,
            horario: Horario,
            estado: Optional[Estado] = None,
            motivoCancelacion: Optional[MotivoCancelacion] = None,
            tipoReserva: Optional[TipoReserva] = None,
            idReserva: Optional[int] = None


    ):

        self.idReserva = idReserva
        self.fechaReserva = fechaReserva
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.motivoCancelacion = motivoCancelacion
        self.estado = estado
        self.tipoReserva = tipoReserva
        self.area = area
        self.usuario = usuario
        self.horario = horario

        if not self.validar_horas(horaInicio, horaFin):
            raise ValueError(
                f"La hora de inicio {horaInicio} debe ser anterior a la hora de fin {horaFin}."
            )

        if not self.validar_fecha_reserva(fechaReserva):
            raise ValueError(
                f"No puedes reservar una fecha pasada. Por favor selecciona una fecha igual o posterior a hoy."
            )

        if not self.validar_cancelacion():
            raise ValueError(
                "Si la reserva está cancelada, debe proporcionar un motivo de cancelación. Si no está cancelada, no debe proporcionar un motivo de cancelación."
            )

 

    def validar_horas(self, horaInicio: time, horaFin: time) -> bool:
        return horaInicio < horaFin

    def validar_fecha_reserva(self, fechaReserva: date) -> bool:
        return fechaReserva >= date.today()

    def validar_cancelacion(self) -> bool:
        if self.estado == Estado.CANCELADA and self.motivoCancelacion is None:
            return False
        if self.estado != Estado.CANCELADA and self.motivoCancelacion is not None:
            return False
        return True


