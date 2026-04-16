from ..interfaces.service.ILicenciaturaService import ILicenciaturaService
from ..interfaces.repository.ILicenciaturaRepository import ILicenciaturaRepository as ILicenciaturaRepo
from app.domain.entities import Licenciatura

class LicenciaturaService(ILicenciaturaService):
    
    def __init__(self, licenciatura_repository: ILicenciaturaRepo):
        self.licenciatura_repository = licenciatura_repository

    def obtenerLicenciatura(self) -> list[Licenciatura]:
        return self.licenciatura_repository.listarLicenciaturas()