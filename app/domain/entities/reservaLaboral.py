from typing import Optional
from .reserva import Reserva, MotivoCancelacion, Estado, TipoReserva
from .licenciatura import Licenciatura
from datetime import time, date
from .area import Area
from .usuario import Usuario
from .horario import Horario


class ReservaLaboral(Reserva):
    def __init__(
        self,
        # Datos del padre
        fechaReserva: date,
        horaInicio: time,
        horaFin: time,
        area: Area,
        usuario: Usuario,
        horario: Horario,
        # Datos específicos
        claseImpartir: str,
        licenciatura: Optional[Licenciatura] = None,
        motivoCancelacion: Optional[MotivoCancelacion] = None,
        idReserva: Optional[int] = None,
        estado: Optional[Estado] = None,
        tipoReserva : Optional[TipoReserva] = None
    ):
        super().__init__(
            fechaReserva=fechaReserva,
            horaInicio=horaInicio,
            horaFin=horaFin,
            estado=estado,
            area=area,
            usuario=usuario,
            horario=horario,
            motivoCancelacion=motivoCancelacion,
            tipoReserva=tipoReserva,
            idReserva=idReserva
        )

        # Atributos propios
        self.claseImpartir = claseImpartir
        self.licenciatura = licenciatura

        if not self.validar_nombre_clase(claseImpartir):
            raise ValueError(
                "El nombre de la clase a impartir no puede estar vacío.")

 
    def validar_nombre_clase(self, claseImpartir: str) -> bool:
        return len(claseImpartir) > 0


