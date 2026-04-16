from pydantic import BaseModel, validator
from datetime import date, time
from app.persistence.models.enums import EstadoExcepcion

class ExcepcionCreateDTO(BaseModel):
    horarioId: int
    fechaInicio: date
    fechaFin: date
    horaInicio: time
    horaFin: time
    estado: EstadoExcepcion