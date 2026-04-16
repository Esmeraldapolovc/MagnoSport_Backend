from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.domain.entities.equipo import Categoria, Estado

class ActualizarEquipoSchema(BaseModel):
    idEquipo: int
    nombre: str
    categoria: Categoria
    fechaRegistro: date
    estado: Estado
    areaId: int
    cantidad: Optional[int] = None
