from dataclasses import dataclass
from typing import Optional
from datetime import date
@dataclass
class AlumnoCreateDTO:
    #Datos de usuario
    nombre: str
    correo: str
    contrasenia: str
    rolId:       int

    #Datos de Alumno
    fechaInicio: date
    nivelId: int
    fechaFin: Optional[date] = None
    licId: Optional[int] = None
    foto:   Optional[str] = None
