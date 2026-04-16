from abc import ABC, abstractmethod
from datetime import date
from app.domain.entities import Noticia

class INoticiaRepository(ABC):

    @abstractmethod
    def agregarNoticia(self, noticia: Noticia) -> Noticia:
        pass 

    @abstractmethod
    def obtenerNoticias(self) -> list[Noticia]:
        pass

    @abstractmethod
    def detalleNoticia(self, idNoticia: int) -> Noticia:
        pass


    @abstractmethod
    def modificarNoticia(self, noticia: Noticia) -> Noticia:
        pass

    @abstractmethod
    def eliminarNoticia(self, idNoticia: int) -> bool:
        pass

    @abstractmethod
    def buscarPorFecha(self, fecha: date) -> list[Noticia]:
        pass