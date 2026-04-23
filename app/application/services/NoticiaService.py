from ..interfaces.service.INoticiasService import INoticiaService
from ..interfaces.repository.INoticiaRepository import INoticiaRepository as INoticiaRepo
from app.application.dtos.noticias import AgregarNoticiaDTO, ActualizarNoticiaDTO, EliminarNoticiaDTO
from app.domain.entities import Noticia, noticia
from datetime import date, datetime
import pendulum
import pytz
from datetime import datetime
class NoticiaService(INoticiaService):
    
    def __init__(self, noticia_repository: INoticiaRepo):
        self.noticia_repository = noticia_repository

    def agregarNoticia(self, dto: AgregarNoticiaDTO) -> str:
        
        # Usar pendulum para zona horaria de México
        ahora_mexico = pendulum.now('America/Mexico_City')
        
        print(f"Fecha con pendulum: {ahora_mexico}")
        print(f"Solo fecha: {ahora_mexico.date()}")
        
        nuevaNoticia = Noticia(
            titulo=dto.titulo,
            descripcion=dto.descripcion,
            estado=1,
            fechaPublicacion=ahora_mexico.date(),
            horaPublicacion=ahora_mexico.time()
        )

        self.noticia_repository.agregarNoticia(nuevaNoticia)

        return "Noticia Publicada"

    

    def obtenerNoticias(self) -> list[Noticia]:
        return self.noticia_repository.obtenerNoticias()
    
    def detalleNoticia(self, idNoticia: int) -> Noticia:
        return self.noticia_repository.detalleNoticia(idNoticia)
    
    def modificarNoticia(self, dto: ActualizarNoticiaDTO) -> str:
        noticiaExistente = self.noticia_repository.detalleNoticia(dto.idNoticia)

        if not noticiaExistente:
            return "Noticia no encontrada"

        mexico_tz = pytz.timezone('America/Mexico_City')
        ahora_mexico = datetime.now(mexico_tz)

        noticiaExistente.titulo = dto.titulo
        noticiaExistente.descripcion = dto.descripcion
        noticiaExistente.fechaPublicacion = ahora_mexico.date()
        noticiaExistente.horaPublicacion = ahora_mexico.time()

        self.noticia_repository.modificarNoticia(noticiaExistente)

        return "Noticia Modificada"
    
    def eliminarNoticia(self, dto: EliminarNoticiaDTO) -> str:
        noticiaExistente = self.noticia_repository.detalleNoticia(dto.idNoticia)

        if not noticiaExistente:
            return "Noticia no encontrada"

        self.noticia_repository.eliminarNoticia(dto.idNoticia)

        return "Noticia Eliminada"
    
    def buscarPorFecha(self, fecha: date) -> list[Noticia]:
        return self.noticia_repository.buscarPorFecha(fecha)
    
    
