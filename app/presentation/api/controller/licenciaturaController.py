from fastapi import HTTPException
from app.application.interfaces.service.ILicenciaturaService import ILicenciaturaService



class LicenciaturaController:
    def __init__(self, service: ILicenciaturaService):
        self.service = service

    def obtenerLicenciatura(self):
        try:
            return self.service.obtenerLicenciatura()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))