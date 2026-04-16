from abc import ABC, abstractmethod
from app.application.dtos.noticias import AgregarNoticiaDTO, ActualizarNoticiaDTO, EliminarNoticiaDTO
from app.domain.entities import Noticia
class INoticiaService(ABC):

    @abstractmethod
    def agregarNoticia(self, dto: AgregarNoticiaDTO) -> str:
        pass

    @abstractmethod
    def obtenerNoticias(self) -> list:
        pass

    @abstractmethod
    def detalleNoticia(self, idNoticia: int) -> Noticia:
        pass    

    @abstractmethod
    def modificarNoticia(self, noticia: ActualizarNoticiaDTO) -> str:
        pass

    @abstractmethod
    def eliminarNoticia(self, dto: EliminarNoticiaDTO) -> str:
        pass

    @abstractmethod
    def buscarPorFecha(self, fecha) -> list[Noticia]:
        pass