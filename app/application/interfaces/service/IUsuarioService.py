from abc import ABC, abstractmethod
from typing import List, Optional
from ...dtos.usuario import UsuarioCreateDTO, UsuarioLoginDTO, UsuarioDeleteDTO, AlumnoCreateDTO, UsuarioUpdateDTO, AlumnoUpdateDTO, AlumnoFilterDTO
from app.domain.entities import Usuario, Alumno


class IUsuarioService(ABC):
    @abstractmethod
    def crearUsuario(self, dto: UsuarioCreateDTO) -> str:
        pass

    @abstractmethod
    def login(self, dto: UsuarioLoginDTO) -> str:
        pass

    @abstractmethod
    def crearAlumno(self, dto: AlumnoCreateDTO) -> str:
        pass

    @abstractmethod
    def actualizarUsuario(self, dto:  UsuarioUpdateDTO) ->str:
        pass

    @abstractmethod
    def actualizarAlumno(self, dto: AlumnoUpdateDTO) -> str:
        pass
    
    @abstractmethod
    def actualizarUsuarioAdmin(self, dto: UsuarioUpdateDTO) -> str:
        pass

    @abstractmethod
    def actualizarAlumnoAdmin(self, dto: AlumnoUpdateDTO) ->str:
        pass

    @abstractmethod
    def eliminarUsuario(self, dto:UsuarioDeleteDTO) -> str:
        pass

    @abstractmethod
    def activarUsuario(self, dto: UsuarioDeleteDTO) -> str:
        pass


    @abstractmethod
    def listarUsuario(self) -> List[Usuario]:
        pass

    @abstractmethod
    def listarAlumno(self)-> List[Alumno]:
        pass


    @abstractmethod
    def filtradoAlumno(self, nombre: Optional[str] = None, correo: Optional[str] = None, 
                   nivelId: Optional[int] = None, licenciaturaId: Optional[int] = None, estado: Optional[int] = None) -> List[Alumno]:
        pass

    @abstractmethod
    def filtradoUsuario(self, nombre: Optional[str] = None, correo: Optional[str] = None, rol: Optional[int] = None, estado: Optional[int] = None) ->List[Usuario]:
        pass

    @abstractmethod
    def obtenerUsuarioPorId(self, idUsuario: int) -> Usuario:
        pass

    @abstractmethod
    def obtenerAlumnoPorId(self, idUsuario:int) ->Alumno :
        pass
