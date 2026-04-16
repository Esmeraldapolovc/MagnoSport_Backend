from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities import NivelAcademico

class INivelAcademicoRepository(ABC):

    @abstractmethod
    def obtenerNivel(self, nivel: NivelAcademico) -> NivelAcademico:
        pass

    @abstractmethod
    def listadoNivel(self) -> list[NivelAcademico]:
        pass