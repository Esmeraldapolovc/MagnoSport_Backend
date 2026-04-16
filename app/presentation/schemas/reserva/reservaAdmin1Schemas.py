from pydantic import BaseModel
from datetime import date, time
from app.persistence.models.enums import tipoReserva as TipoReserva
from typing import Optional, List
class ReservaAdmin1Schemas(BaseModel):
   
    fechaReserva: date
    horaInicio: time
    horaFin: time
    areaId: int
    idUsuario: int
    horarioId: int
    tipoReserva: Optional[TipoReserva] = None
    claseImpartir: Optional[str] = None
    licId: Optional[int] = None

     # Datos para reserva de quipo (Cardio)
    equipoId: Optional[List[int]] = None
