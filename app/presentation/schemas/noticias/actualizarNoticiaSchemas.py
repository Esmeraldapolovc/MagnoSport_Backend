from pydantic import BaseModel

class ActualizarNoticiaSchema(BaseModel):
        idNoticia: int
        titulo: str
        descripcion: str

