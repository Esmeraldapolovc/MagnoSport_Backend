from pydantic import BaseModel

class ReservaEquipoDTO(BaseModel):
    id_reserva: int
    id_equipo: int