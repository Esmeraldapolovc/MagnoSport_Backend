from pydantic import BaseModel
from datetime import date, time
from typing import List
from app.persistence.models.enums import EstadoHorario

class HorarioCreateDTO(BaseModel):
    fechaInicio: date
    fechaFin: date
    horaInicio: time
    horaFin: time
    dias: List[int]  
    estado: EstadoHorario