from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UsuarioCreateDTO:
    nombre: str
    correo: str
    contrasenia: str
    rolId:       int
    foto:   Optional[str] = None
