from pydantic import BaseModel

class ReservaEquipoSchema(BaseModel):
    id_reserva: int
    id_equipo: int