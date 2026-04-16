from typing import Optional
from .nivelAcademinco import NivelAcademico


class Licenciatura:

    def __init__(
        self,
        nombreLic: str,
        nivel: NivelAcademico,
        idLicenciatura: Optional[int] = None

    ):

        self.idLicenciatura = idLicenciatura
        self.nombreLic = nombreLic.upper()
        self.nivel = nivel
