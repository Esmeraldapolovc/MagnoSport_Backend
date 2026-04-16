from typing import Optional
from datetime import date, time
from enum import Enum
from .horario import Horario


class Estado(Enum):
    CERRADO = "Cerrado"
    ABIERTO = "Abierto"


class ExcepcionHorario:

    def __init__(self,
                 fechaInicio: date,
                 fechaFin: date,
                 horaInicio: time,
                 horaFin: time,
                 estado: Estado,
                 horario: Horario,
                 idExcepcion: Optional[int] = None):

        self.idExcepcion = idExcepcion
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.estado = estado
        self.horario = horario

        if not self.validar_fechas(fechaInicio, fechaFin):
            raise ValueError(
                "La fecha de inicio debe ser anterior o igual a la fecha de fin."
            )
        if not self.validar_horas(horaInicio, horaFin):
            raise ValueError(
                f"La hora de inicio {horaInicio} debe ser anterior a la hora de fin {horaFin}."
            )

    def validar_fechas(self, fechaInicio: date, fechaFin: date) -> bool:
        return fechaInicio <= fechaFin

    def validar_horas(self, horaInicio: time, horaFin: time) -> bool:
        return horaInicio < horaFin
