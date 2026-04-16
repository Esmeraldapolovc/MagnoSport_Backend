from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities import Usuario, Alumno


class IUsuarioRepository(ABC):

    @abstractmethod
    def CrearUsuario(self, usuario: Usuario) -> Optional[Usuario]:
        pass
    @abstractmethod
    def buscarPorCorreo(self, correo: str) -> bool:
        pass
   

    @abstractmethod
    def login(self, correo: str) -> Usuario:
        pass

    @abstractmethod
    def crearAlumno(self, alumno: Alumno) -> Alumno:
        pass

    def obtenerUsuarioPorId(self, idUsuario: int) -> Usuario:
        pass

    def obtenerAlumnoPorId(self, idUsuario:int) ->Optional[Alumno] :
        pass

    @abstractmethod
    def actualizarUsuario(self, usuario: Usuario) -> Optional[Usuario]:
        pass
    
    def actualizarAlumno(self, alumno: Alumno) -> Optional[Alumno]:
        pass
    
    def actualizarUsuarioAdmin (self, usuario: Usuario) -> Optional[Usuario]:
        pass

    def actualizarAlumnoAdmin(self, alumno: Alumno) -> Optional[Alumno]:
        pass

    def eliminarUsuario(self, idUsuario: int) -> bool:
        pass

    def listarUsuarios(self) -> List[Usuario]:
        pass

    @abstractmethod
    def listarAlumno(self)-> List[Alumno]:
        pass

    @abstractmethod
    def filtradoAlumno(self, nombre: Optional[str] = None, correo: Optional[str] = None, nivelId: Optional[int] = None, 
        licenciaturaId: Optional[int] = None, estado: Optional[int] = None) -> List[Alumno]:
      pass

    @abstractmethod
    def filtradoUsuario(self, nombre: Optional[str] = None, correo: Optional[str] = None, rol: Optional[int] = None, estado: Optional[int] = None) ->List[Usuario]:
        pass

    @abstractmethod
    def activarUsuario(self, idUsuario: int) -> bool:
        pass

    @abstractmethod
    def crearAlumno1 (self, alumno: Alumno) -> Alumno:
        pass