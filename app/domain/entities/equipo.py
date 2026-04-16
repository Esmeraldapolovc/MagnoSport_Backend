from typing import Optional
from enum import Enum
from datetime import date
from .area import Area
# Enums


class Categoria(Enum):
    MAQUINA = "Máquina"
    MATERIAL = "Material"


class Estado(Enum):
    DISPONIBLE = "Disponible"
    NO_DISPONIBLE = "No disponible"
    MANTENIMIENTO = "Mantenimiento"
    FUERA_DE_SERVICIO = "Fuera de servicio"

# Entidad


class Equipo:

    def __init__(self,
                 nombre: str,
                 cantidad: int,
                 categoria: Categoria,
                 fechaRegistro: date,
                 estado: Estado,
                 area: Area,
                 idEquipo: Optional[int] = None
                 ):

        self.idEquipo = idEquipo
        self.nombre = nombre
        self.cantidad = cantidad
        self.categoria = categoria
        self.fechaRegistro = fechaRegistro
        self.estado = estado
        self.area = area

        if not self.validar_cantidad(cantidad):
            raise ValueError(
                f"La cantidad {cantidad} debe ser un número entero no negativo."
            )

    def validar_cantidad(self, cantidad: int) -> bool:
        return cantidad >= 0

    def estado_operativo(self) -> bool:
        return self.estado == Estado.DISPONIBLE
