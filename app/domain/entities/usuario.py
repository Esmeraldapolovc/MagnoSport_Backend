from typing import Optional
from .rol import Rol
import re


class Usuario:

    def __init__(
            self,
            nombre: str,
            correo: str,
            foto: str,
            rol: Rol,
            idUsuario: Optional[int] = None,
            estatus: Optional[int] = None,
            contrasenia: Optional[str] = None



    ):

        # validar formato de correo electronico
        if not self.validar_correo(correo):
            raise ValueError(
                f"El correo electrónico {correo} no tiene un formato válido.")

        if contrasenia is not None:
          if not self.validar_contrasenia(contrasenia):
              raise ValueError(
                "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial.")

        self.idUsuario = idUsuario
        self.nombre = nombre.upper()
        self.correo = correo.lower()
        self.foto = foto
        self.contrasenia = contrasenia
        self.estatus = estatus
        self.rol = rol

    def validar_correo(self, correo: str) -> bool:
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, correo) is not None

    def validar_contrasenia(self, contrasenia: str) -> bool:
        
        if contrasenia.startswith("$2"):
            return True
            
        patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(patron, contrasenia) is not None
