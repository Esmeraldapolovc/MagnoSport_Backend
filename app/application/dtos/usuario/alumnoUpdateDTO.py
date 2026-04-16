from dataclasses import dataclass
from typing import Optional
from datetime import date
@dataclass(frozen = True)
class AlumnoUpdateDTO:
    idUsuario: int
    nombre: str
    correo: str
    rolId: int
    nivelId: int
    fechaInicio: date
    contrasenia: Optional[str] = None
    contraseniaActual:  Optional[str] = None
    fechaFin: Optional[date] = None
    licId: Optional[int] = None
    foto: Optional[str] = ""