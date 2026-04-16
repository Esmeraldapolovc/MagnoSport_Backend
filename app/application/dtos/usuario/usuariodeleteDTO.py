from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UsuarioDeleteDTO:
    idUsuario: int