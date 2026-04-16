from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class AlumnoFilterDTO:
        nombre: Optional[str] = None, 
        correo: Optional[str] = None, 
        nivelId: Optional[int] = None, 
        licenciaturaId: Optional[int] = None