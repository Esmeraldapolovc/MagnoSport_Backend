from pydantic import BaseModel

class AgregarNoticiaSchema(BaseModel):
        titulo: str
        descripcion: str

