from typing import Optional


class Area:

    def __init__(
        self,
        nombreArea: str,
        idArea: Optional[int] = None
    ):

        self.idArea = idArea
        self.nombreArea = nombreArea.upper()
