from app.application.interfaces.repository.ILicenciaturaRepository import ILicenciaturaRepository
from app.domain.entities import Licenciatura
from app.persistence.models.licenciatura import Licenciatura as LicModel
from sqlalchemy.orm import Session

class LicenciaturaRepository(ILicenciaturaRepository):
    def __init__(self, db: Session):
                self.db = db



    def obtenerLicenciatura(self, lic: int) -> Licenciatura:
            dbLic = self.db.query(LicModel).filter(LicModel.idLicenciatura == lic).first()

            if not dbLic:
                    return None
            
            return Licenciatura(idLicenciatura=dbLic.idLicenciatura, nombreLic=dbLic.nombreLic, nivel=dbLic.nivelId)
    
    def listarLicenciaturas(self) -> list[Licenciatura]:
            dbLics = self.db.query(LicModel).all()
            return [Licenciatura(idLicenciatura=lic.idLicenciatura, nombreLic=lic.nombreLic, nivel=lic.nivelId) for lic in dbLics]