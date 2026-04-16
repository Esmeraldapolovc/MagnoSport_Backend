from pydantic import BaseModel
from datetime import date, time
from app.persistence.models.enums import EstadoExcepcion

class ExcepcionSchema(BaseModel):
    horarioId: int
    fechaInicio: date
    fechaFin: date
    horaInicio: time
    horaFin: time
    estado: EstadoExcepcion