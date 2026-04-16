from pydantic import BaseModel
from datetime import date, time

class  ObtenerAgendaDTO(BaseModel):
    usuarioId: int