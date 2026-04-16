from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioLoginSchema(BaseModel):
    correo: str
    contrasenia: str
