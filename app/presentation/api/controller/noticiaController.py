from datetime import date

from fastapi import HTTPException
from app.application.dtos.noticias.eliminarNoticiaDTO import EliminarNoticiaDTO
from app.application.interfaces.service.INoticiasService import INoticiaService
from app.application.dtos.noticias import AgregarNoticiaDTO, ActualizarNoticiaDTO
from ...schemas.noticias import AgregarNoticiaSchema, ActualizarNoticiaSchema, EliminarNoticiaSchema

class NoticiaController:
    def __init__(self, service: INoticiaService):
        self.service = service

    def agregarNoticia(self, request: AgregarNoticiaSchema):
        try:
            dto = AgregarNoticiaDTO(
                titulo=request.titulo,
                descripcion=request.descripcion
            )
            return self.service.agregarNoticia(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    
    def obtenerNoticias(self):
        try:
            return self.service.obtenerNoticias()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        

    def detalleNoticia(self, idNoticia: int):
        try:
            return self.service.detalleNoticia(idNoticia)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        

    def modificarNoticia(self, request: ActualizarNoticiaSchema):
        try:
            dto = ActualizarNoticiaDTO(
                idNoticia=request.idNoticia,
                titulo=request.titulo,
                descripcion=request.descripcion
            )
            return self.service.modificarNoticia(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def eliminarNoticia(self, request:EliminarNoticiaSchema):
        try:
            dto = EliminarNoticiaDTO(
                idNoticia=request.idNoticia
            )
            return self.service.eliminarNoticia(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        
    def buscarPorFecha(self, fecha: date):
        try:
            return self.service.buscarPorFecha(fecha)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    