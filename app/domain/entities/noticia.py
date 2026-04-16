from typing import Optional
from datetime import time, date


class Noticia:
    def __init__(
            self,
            titulo: str,
            descripcion: str,
            estado: int,
            fechaPublicacion: date,
            horaPublicacion: time,
            idNoticia: Optional[int] = None
    ):

        self.idNoticia = idNoticia
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.fechaPublicacion = fechaPublicacion
        self.horaPublicacion = horaPublicacion

        if not self.validar_estado(estado):
            raise ValueError(
                f"El estado {estado} no es válido. Debe ser 0 (Inactiva) o 1 (Activa)."
            )

        if not self.validar_fecha_publicacion(fechaPublicacion):
            raise ValueError(
                f"La fecha de publicación {fechaPublicacion} no puede ser futura."
            )

    # validar estado
    def validar_estado(self, estado: int) -> bool:
        return estado in [0, 1]

    # valida que la fecha de publicación no sea futura
    def validar_fecha_publicacion(self, fechaPublicacion: date) -> bool:
        return fechaPublicacion <= date.today()
