from dataclasses import dataclass
from typing import Optional
@dataclass(frozen=True)
class UsuarioUpdateDTO:
    idUsuario: int
    nombre: str
    correo: str
    rolId:       int
    contrasenia:  Optional[str] = None
    contraseniaActual:  Optional[str] = None
    foto:   Optional[str] = None