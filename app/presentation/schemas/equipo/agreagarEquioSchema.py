from pydantic import BaseModel
from app.domain.entities.equipo import Categoria
from typing import Optional
class AgregarEquipoSchema(BaseModel):
    nombre: str
    categoria: Categoria
    areaId: int
    cantidad: Optional[int] = None