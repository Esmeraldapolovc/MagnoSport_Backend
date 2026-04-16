from abc import ABC, abstractmethod
from app.domain.entities import NivelAcademico
class INivelService(ABC):

    @abstractmethod
    def listadoNivel(self) -> list[NivelAcademico]:
        pass