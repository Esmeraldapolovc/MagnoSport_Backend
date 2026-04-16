from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class ReservaDetalleDTO:
    idReserva: int
    areaId: int
    estado: Any
    usuario: Any
    reserva_equipos: List[Any]
    reserva_laboral: Optional[Any] = None
    tipo_reserva: Optional[str] = None 
