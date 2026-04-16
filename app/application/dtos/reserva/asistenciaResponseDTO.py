from dataclasses import dataclass

@dataclass
class AsistenciaResponseDTO:
    idReserva: int
    mensaje: str
    nuevo_estado: str
    exito: bool