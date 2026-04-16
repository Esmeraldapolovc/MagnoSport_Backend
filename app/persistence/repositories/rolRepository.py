from app.application.interfaces.repository.IRolRepository import IRolRepository
from app.domain.entities import Rol
from app.persistence.models import Rol as RolModel
from sqlalchemy.orm import Session


class RolRepository(IRolRepository):

    def __init__(self, db: Session):
        self.db = db

    def obtenerRol(self, rol: int) -> Rol:
        dbRol = self.db.query(RolModel).filter(RolModel.idRol == rol).first()

        if not dbRol:
            return None

        return Rol(idRol=dbRol.idRol, nombreRol=dbRol.nombreRol)
