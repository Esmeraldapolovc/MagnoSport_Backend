from pydantic import BaseModel

class AgregarNoticiaDTO(BaseModel):
    titulo: str
    descripcion: str
