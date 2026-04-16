from typing import Optional


class Dia:
    def __init__(
        self,
        nombreDia: str,
        idDia: Optional[int] = None
    ):

        self.idDia = idDia
        self.nombreDia = nombreDia.upper()
