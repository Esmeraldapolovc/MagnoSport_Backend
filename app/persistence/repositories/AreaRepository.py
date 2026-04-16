from app.application.interfaces.repository.IAreaRepository import IAreaRepository
from app.persistence.models.area import Area as AreaModel
from sqlalchemy.orm import Session

class AreaRepository(IAreaRepository):
    def __init__(self, db: Session):
        self.db = db

    def opteberAreaPorId(self, idArea: int):
        return self.db.query(AreaModel).filter(AreaModel.idArea == idArea).first()
