from fastapi import HTTPException

from app.application.interfaces.service.INivelService import INivelService


class NivelController:
    def __init__(self, service: INivelService):
        self.service = service


    def obtenerNivel(self):
        try:
            return self.service.listadoNivel()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
            