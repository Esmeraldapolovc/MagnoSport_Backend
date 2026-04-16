from typing import Optional


class NivelAcademico:

    def __init__(
        self,
        nombreNivel: str,
        idNivel: Optional[int] = None
    ):

        self.idNivel = idNivel
        self.nombreNivel = nombreNivel.upper()
