from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
class AlumnoCreateSchema(BaseModel):
    nombre: str
    correo: EmailStr
    contrasenia: str
    foto: Optional[str] = None
    rolId: int

     #Datos de Alumno
    fechaInicio: date
    fechaFin: Optional[date] = None
    nivelId: int
    licId: Optional[int] = None 