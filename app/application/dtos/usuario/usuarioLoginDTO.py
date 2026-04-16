from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UsuarioLoginDTO:
    correo: str
    contrasenia: str
