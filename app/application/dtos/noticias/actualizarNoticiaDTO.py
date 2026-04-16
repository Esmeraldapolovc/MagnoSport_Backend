from pydantic import BaseModel

class ActualizarNoticiaDTO(BaseModel):
    idNoticia: int
    titulo: str
    descripcion: str
