from pydantic import BaseModel
from datetime import date, time
from typing import Optional, List
from app.persistence.models.enums import tipoReserva as TipoReserva

class ReservaAlumnoCreateDTO(BaseModel):
    fechaReserva: date
    horaInicio: time
    horaFin: time
    areaId: int
    usuarioId: int
    horarioId: int

    # Datos para reserva Laboral
    tipoReserva: Optional[TipoReserva] = None
    claseImpartir: Optional[str] = None
    licId: Optional[int] = None
     # Datos para reserva de quipo (Cardio)
    equipoId: Optional[List[int]] = None
