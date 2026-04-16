from pydantic import BaseModel
from datetime import date, time
from typing import List
from app.persistence.models.enums import EstadoHorario

class HorarioCreateSchema(BaseModel):
    fechaInicio: date
    fechaFin: date
    horaInicio: time
    horaFin: time
    dias: List[int]  
    estado : EstadoHorario
    class Config:
        json_schema_extra = {
            "example": {
                "fechaInicio": "2026-03-01",
                "fechaFin": "2026-12-31",
                "horaInicio": "08:00:00",
                "horaFin": "16:00:00",
                "dias": [1, 2, 3, 4, 5],
                "estado": "Abierto"
            }
        }