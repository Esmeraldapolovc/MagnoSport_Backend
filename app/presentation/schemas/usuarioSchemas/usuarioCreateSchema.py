from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioCreateSchema(BaseModel):
    nombre: str
    correo: EmailStr
    contrasenia: str
    foto: Optional[str] = None
    rolId: int
