from typing import Optional
from .usuario import Usuario
from .nivelAcademinco import NivelAcademico
from .licenciatura import Licenciatura
from .rol import Rol
from datetime import date


class Alumno(Usuario):

    def __init__(
            self,
            # Datos heredados de Usuario
            nombre: str,
            correo: str,
            foto: str,
            contrasenia: str,
            rol: Rol,
            # Datos específicos de Alumno
            fechaInicio: date,
            nivel: NivelAcademico,
            licenciatura: Optional[Licenciatura] = None,
            fechaFin: Optional[date] = None,
            idUsuario: Optional[int] = None,
            estatus: Optional[int] = None,

    ):

        super().__init__(
            nombre=nombre,
            correo=correo,
            foto=foto,
            contrasenia=contrasenia,
            rol=rol,
            idUsuario=idUsuario,
            estatus=estatus)

        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.nivel = nivel
        self.licenciatura = licenciatura

        if not self.validar_fechas(fechaInicio, fechaFin):
            raise ValueError(
                "La fecha de inicio debe ser anterior a la fecha de fin."
            )

    def validar_fechas(self, fechaInicio: date, fechaFin: Optional[date]) -> bool:
        if fechaFin is not None:
            return fechaInicio < fechaFin
        return True
