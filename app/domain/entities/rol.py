from typing import Optional


class Rol:

    def __init__(
            self,
            nombreRol: str,
            idRol: Optional[int] = None
    ):

        self.idRol = idRol
        self.nombreRol = nombreRol.upper()

        # compara dos objetos de tipo Rol, se consideran iguales si tienen el mismo nombreRol
        def __eq__(self, otroRol):
            if not isinstance(otroRol, Rol):
                return False
            return self.nombreRol == otroRol.nombreRol
