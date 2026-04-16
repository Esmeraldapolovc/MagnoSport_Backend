from app.application.interfaces.repository.INivelAcademicoRepository import INivelAcademicoRepository
from app.domain.entities import NivelAcademico
from app.persistence.models.nivelAcademico import NivelAcademico as NivelModel
from sqlalchemy.orm import Session

class NivelAcademicoRepository(INivelAcademicoRepository):

    
    def __init__(self, db: Session):
        self.db = db

    def obtenerNivel(self,nivel: int ) -> NivelAcademico:
        dbNivel = self.db.query(NivelModel).filter(NivelModel.idNivel == nivel).first()


        if not nivel:
            return None
        
        return NivelAcademico(nombreNivel=dbNivel.nombreNivel, idNivel=dbNivel.idNivel)
    

    def listadoNivel(self) -> list[NivelAcademico]:
       dbNivel = self.db.query(NivelModel).all()

       return [NivelAcademico(idNivel=nivel.idNivel, nombreNivel=nivel.nombreNivel) for nivel in dbNivel]
      


