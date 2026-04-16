from pydantic import BaseModel

class ReservaDeleteDTO(BaseModel):
    idReserva: int
    usuarioId: int