from enum import Enum
from typing import Optional
from datetime import date, time, datetime

# Enum para representar el estado del horario


class Estado(Enum):
    CERRADO = "Cerrado"
    ABIERTO = "Abierto"


class Horario:

    def __init__(
        self,
        fechaInicio: date,
        fechaFin: date,
        horaInicio: time,
        horaFin: time,
        estado: Estado,
        idHorario: Optional[int] = None
    ):

        self.idHorario = idHorario
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.estado = estado

        if not self.validar_fechas(fechaInicio, fechaFin):
            raise ValueError(
                "La fecha de inicio debe ser anterior o igual a la fecha de fin."
            )

        if not self.validar_horas(horaInicio, horaFin):
            raise ValueError(
                f"La hora de inicio {horaInicio} debe ser anterior a la hora de fin {horaFin}."
            )
        
        if not self.validar_fecha_futura(fechaInicio):
            raise ValueError(
                f"La fecha de inicio {fechaInicio} no puede ser anterior a la fecha actual."
            )

    # metodos de reglas de negocio para validar fechas y horas
    def validar_fechas(self, fechaInicio: date, fechaFin: date) -> bool:
        return fechaInicio <= fechaFin

    def validar_horas(self, horaInicio: time, horaFin: time) -> bool:
        return horaInicio < horaFin
    
    def validar_fecha_futura(self, fechaInicio: date) -> bool:
        return fechaInicio >= date.today()
