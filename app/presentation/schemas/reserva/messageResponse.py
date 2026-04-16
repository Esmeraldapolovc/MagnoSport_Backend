from pydantic import BaseModel

class AsistenciaExitoSchema(BaseModel):
    idReserva: int
    mensaje: str
    nuevo_estado: str

class ErrorSchema(BaseModel):
    detail: str