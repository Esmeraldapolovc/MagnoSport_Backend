from abc import ABC, abstractmethod
from app.application.dtos.horario  import HorarioCreateDTO, ExcepcionCreateDTO
from app.domain.entities import Horario
from typing import List
from datetime import date

class IHorarioService(ABC):

    @abstractmethod
    def crearHorario(self, dto: HorarioCreateDTO) -> dict:
        pass

    def listarHorarios(self) -> List[Horario]:
        pass

    @abstractmethod
    def crearExcepcion(self, dto: ExcepcionCreateDTO) -> str:
      pass

    @abstractmethod
    def obtenerEstadoPorFecha(self, fecha: date):
        pass
    