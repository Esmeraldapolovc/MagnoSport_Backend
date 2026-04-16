import enum

from sqlalchemy import Enum

# Enums para los modelos de la base de datos


class EstadoHorario(enum.Enum):  # Enum para el estado de horario
    CERRADO = "Cerrado"
    ABIERTO = "Abierto"


class EstadoExcepcion(enum.Enum):  # Enum para el estado de excepción de horario
    CERRADO = "Cerrado"
    ABIERTO = "Abierto"


# Enum para el motivo de cancelación de reserva
class MotivoCancelacion(enum.Enum):
    CANCELACION_POR_USUARIO = "Cancelada por el usuario"
    CANCELACION_POR_RETRASO = "Cancelada por retraso"
    CANCELACION_POR_EXCEPCION = "Cancelada por excepcion"


class EstadoReserva(enum.Enum):  # Enum para el estado de reserva
    PENDIENTE = "Pendiente"
    ASISTIO = "Asistió"
    CANCELADO = "Cancelado"


class tipoReserva(enum.Enum):  # Enum para el tipo de reserva
    LABORAL = "Laboral"
    PERSONAL = "Personal"


class CategoriaEquipo(enum.Enum):  # Enum para la categoría de equipo
    MAQUINA = "Máquina"
    MATERIAL = "Material"


class EstadoEquipo(enum.Enum):  # Enum para el estado de equipo
    DISPONIBLE = "Disponible"
    NO_DISPONIBLE = "No Disponible"
    MANTENIMIENTO = "Mantenimiento"
    FUERA_DE_SERVICIO = "Fuera de Servicio"


class EstadoUsoEquipo(enum.Enum):  # Enum para el estado de uso de equipo
    PENDIENTE = 'Pendiente'
    EN_USO = "En Uso"
    FIN_USO = "Fin Uso"
