from typing import Optional
from .dia import Dia
from .horario import Horario


class HorarioDia:

    def __init__(
        self,
        idHorarioDia: Optional[int] = None,
        horario: Optional[Horario] = None,
        dia: Optional[Dia] = None
    ):

        self.idHorarioDia = idHorarioDia
        self.horario = horario
        self.dia = dia
