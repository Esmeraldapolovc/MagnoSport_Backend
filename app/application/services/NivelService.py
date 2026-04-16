from ..interfaces.service.INivelService import INivelService
from ..interfaces.repository.INivelAcademicoRepository import INivelAcademicoRepository
from app.domain.entities import NivelAcademico
class NivelService(INivelService):

   def __init__(self, repository: INivelAcademicoRepository ):
          self.repository = repository


   def listadoNivel(self) -> list[NivelAcademico]:

        return self.repository.listadoNivel()
         