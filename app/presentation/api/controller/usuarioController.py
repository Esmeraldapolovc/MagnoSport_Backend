from fastapi import HTTPException
from app.application.interfaces.service.IUsuarioService import IUsuarioService
from app.application.dtos.usuario import UsuarioCreateDTO, UsuarioLoginDTO, UsuarioDeleteDTO, UsuarioUpdateDTO, AlumnoFilterDTO,AlumnoCreateDTO, AlumnoUpdateDTO
from ...schemas.usuarioSchemas import UsuarioLoginSchema, UsuarioDeleteSchema
from fastapi import HTTPException, UploadFile, File, Form
from typing import Optional
from datetime import date
class UsuarioController:
    def __init__(self, service: IUsuarioService):
        self.service = service

   ##################
    def login(self, request: UsuarioLoginSchema):
        try:
            dto = UsuarioLoginDTO(
                correo=request.correo,
                contrasenia=request.contrasenia
            )
            return self.service.login(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    ################

    def crearUsuario(self, nombre: str = Form(...),correo: str = Form(...),
    contrasenia: str = Form(...),rolId: int = Form(...),foto: Optional[UploadFile] = File(None)):
        try:
            dto = UsuarioCreateDTO(
            nombre=nombre,
            correo=correo,
            foto="", 
            contrasenia=contrasenia,
            rolId=rolId
        )
            return self.service.crearUsuario(dto, foto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        
    ########
    def crearAlumno(self, 
        nombre: str, 
        correo: str, 
        contrasenia: str, 
        rolId: int, 
        fechaInicio: date, 
        fechaFin: Optional[date], 
        nivelId: int, 
        licId: Optional[int], 
        foto: Optional[UploadFile] = File(None)):
        try:
            dto = AlumnoCreateDTO(
                nombre=nombre,
                correo=correo,
                contrasenia=contrasenia,
                rolId=rolId,
                fechaInicio=fechaInicio,
                fechaFin=fechaFin,
                nivelId=nivelId,
                licId=licId,
                foto="" 
        )

            return self.service.crearAlumno(dto, foto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) 
    ####
    def actualizarUsuario(self, 
        idUsuario: int, #
        nombre: str,
        correo: str,
        contrasenia: Optional[str],
        rolId: int,
        contraseniaActual: Optional[str],
        foto: Optional[UploadFile] = File(None)
    ):
        try:
        
            dto = UsuarioUpdateDTO(
                idUsuario=idUsuario, 
                nombre=nombre,
                correo=correo,
                contrasenia=contrasenia,
                rolId=rolId,
                contraseniaActual=contraseniaActual,
                foto="" 
            )
            
            return self.service.actualizarUsuario(dto, foto)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    ###
    def actualizarAlumno(self,     idUsuario: int,
    nombre: str,
    correo: str,
    rolId: int,
    nivelId: int,
    fechaInicio: date,
    contrasenia: Optional[str] ,
    contraseniaActual: Optional[str] ,
    licId: Optional[int] ,
    fechaFin: Optional[date] ,
    foto: Optional[UploadFile] = File(None)):
        try:
            dto = AlumnoUpdateDTO(
                idUsuario=idUsuario,
                nombre=nombre,
                correo=correo,
                rolId=rolId,
                nivelId=nivelId,
                fechaInicio=fechaInicio,
                contrasenia= contrasenia,
                contraseniaActual=contraseniaActual,
                licId= licId,
                fechaFin=fechaFin,
                foto = ""

            )
            return self.service.actualizarAlumno(dto, foto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    ####
    def actualizarUsuarioAdmin(self, 
        idUsuario: int = Form(...), #
        nombre: str = Form(...),
        correo: str = Form(...),
        rolId: int = Form(...),
         contrasenia: Optional[str] = Form(None),
        foto: Optional[UploadFile] = File(None)
    ):
        try:
        
            dto = UsuarioUpdateDTO(
                idUsuario=idUsuario, 
                nombre=nombre,
                correo=correo,
                contrasenia=contrasenia,
                rolId=rolId,
                contraseniaActual=None,
                foto="" 
            )
            
            return self.service.actualizarUsuarioAdmin(dto, foto)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def actualizarAlumnoAdmin(self,     idUsuario: int = Form(...),
    nombre: str = Form(...),
    correo: str = Form(...),
    rolId: int = Form(...),
    nivelId: int = Form(...),
    fechaInicio: date = Form(...),
    contrasenia: Optional[str] = Form(None),
    licId: Optional[int] = Form(None),
    fechaFin: Optional[date] = Form(None),
    foto: Optional[UploadFile] = File(None)):
        try:
            dto = AlumnoUpdateDTO(
                idUsuario=idUsuario,
                nombre=nombre,
                correo=correo,
                rolId=rolId,
                nivelId=nivelId,
                fechaInicio=fechaInicio,
                contrasenia= contrasenia,
                contraseniaActual = None,
                licId= licId,
                fechaFin=fechaFin,
                foto = ""

            )
            return self.service.actualizarAlumnoAdmin(dto, foto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        

    def eliminarUsuario(self, request:UsuarioDeleteSchema):
        try:
            dto = UsuarioDeleteDTO(
                idUsuario=request.idUsuario
            )
            return self.service.eliminarUsuario(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        

    def activarUsuario(self, request:UsuarioDeleteSchema):
        try:
            dto = UsuarioDeleteDTO(
                idUsuario=request.idUsuario
            )
            return self.service.activarUsuario(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
###############
    def listarUsuario(self):
       try:
          return self.service.listarUsuario()

       except ValueError as e:
           raise HTTPException(status_code=400, detail=str(e))
       
################
    def listarAlumno(self):
        try:
            return self.service.listarAlumno()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        

    def filtrandoAlumno(self, nombre: Optional[str] = None, correo: Optional[str] = None, 
                     nivelId: Optional[int] = None, licenciaturaId: Optional[int] = None, estado: Optional[int] = None):
        try:
  
            return self.service.filtradoAlumno(nombre, correo, nivelId, licenciaturaId, estado)
        except ValueError as e:
          raise HTTPException(status_code=400, detail=str(e))
        
    
    def filtrandoUsuario(self, nombre: Optional[str] = None, correo: Optional[str] = None, 
                     rol: Optional[int] = None, estado: Optional[int] = None):
        try:
  
            return self.service.filtradoUsuario(nombre, correo, rol, estado)
        except ValueError as e:
          raise HTTPException(status_code=400, detail=str(e))
        

    def obtenerUsuarioPorId(self, idUsuario:int):
        try:
            return self.service.obtenerUsuarioPorId(idUsuario)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def obtenerAlumnorioPorId(self, idUsuario:int):
        try:
            return self.service.obtenerAlumnoPorId(idUsuario)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        

        
