from fastapi import APIRouter, Depends, File, UploadFile, Form, Query
from typing import Optional
from ..controller.usuarioController import UsuarioController
from app.presentation.schemas.usuarioSchemas import  UsuarioLoginSchema,UsuarioDeleteSchema, AlumnoCreateSchema
from app.infrastructure.dependencies import get_usuario_service, get_current_user, require_admin
from datetime import date





router = APIRouter(prefix="/usuarios", tags=["Usuario"])

@router.post("/registroUsuario")
def crearUsuario(
    nombre: str = Form(...),
    correo: str = Form(...),
    contrasenia: str = Form(...),
    rolId: int = Form(...),
    foto: Optional[UploadFile] = File(None),
    service=Depends(get_usuario_service)
):
    controller = UsuarioController(service)
    # Ahora le pasas los campos individuales al controlador
    return controller.crearUsuario(
        nombre=nombre, 
        correo=correo, 
        contrasenia=contrasenia, 
        rolId=rolId, 
        foto=foto
    )

@router.post("/login")
def login(
    request: UsuarioLoginSchema,
    service=Depends(get_usuario_service)
):

    controller = UsuarioController(service)
    return controller.login(request)

@router.post("/registroAlumno")
def crearAlumno(
    nombre: str = Form(...),
    correo: str = Form(...),
    contrasenia: str = Form(...),
    rolId: int = Form(...),
    fechaInicio: date = Form(...),
    nivelId: int = Form(...),
    licId: Optional[int] = Form(None),
    fechaFin: Optional[date] = Form(None),
    foto: Optional[UploadFile] = File(None), 
    service=Depends(get_usuario_service)
):
    controller = UsuarioController(service)
    return controller.crearAlumno(
        nombre=nombre,
        correo=correo,
        contrasenia=contrasenia,
        rolId=rolId,
        fechaInicio=fechaInicio,
        fechaFin=fechaFin,
        nivelId=nivelId,
        licId=licId,
        foto=foto
    )

@router.put("/actuaizarUsuario")
def actuaizarUsuario(
    nombre: str = Form(...),
    correo: str = Form(...),
    contrasenia: str = Form(None),
    rolId: int = Form(...),
    contraseniaActual: str = Form (None),
    foto: Optional[UploadFile] = File(None), 
    usuario = Depends(get_current_user),

    service=Depends(get_usuario_service)
):
    
    
    controller = UsuarioController(service)
    return controller.actualizarUsuario(
        usuario["idUsuario"],
        nombre=nombre,
        correo=correo,
        contrasenia=contrasenia,
        rolId=rolId,
        contraseniaActual = contraseniaActual,
        foto=foto
    )

@router.put("/actualizarAlumno")
def actualizarAlumno(
    nombre: str = Form(...),
    correo: str = Form(...),
    rolId: int = Form(...),
    nivelId: int = Form(...),
    fechaInicio: date = Form(...),
    contrasenia: Optional[str] = Form(None),
    contraseniaActual:  Optional[str] = Form(None),
    licId: Optional[int] = Form(None),
    fechaFin: Optional[date] = Form(None),
    foto: Optional[UploadFile] = File(None),
    usuario = Depends(get_current_user),
    service=Depends(get_usuario_service)
):
    controller = UsuarioController(service)
    return controller.actualizarAlumno(usuario["idUsuario"],
                                       nombre= nombre,
                                       correo=correo,
                                       rolId=rolId,
                                       nivelId=nivelId,
                                       fechaInicio=fechaInicio,
                                       contrasenia=contrasenia,
                                       contraseniaActual = contraseniaActual,
                                       licId=licId,
                                       fechaFin=fechaFin,
                                       foto = foto)


@router.put("/actuaizarUsuarioAdmin")
def actuaizarUsuarioAdmin(
    idUsuario: int = Form(...),
    nombre: str = Form(...),
    correo: str = Form(...),
    rolId: int = Form(...),
    contrasenia: Optional[str] = Form(None),
    foto: Optional[UploadFile] = File(None), 
    usuario = Depends(require_admin),
    service=Depends(get_usuario_service)
):
    
    controller = UsuarioController(service)
    return controller.actualizarUsuarioAdmin(
        idUsuario = idUsuario,
        nombre=nombre,
        correo=correo,
        contrasenia=contrasenia,
        rolId=rolId,
        foto=foto
    )

@router.put("/actualizarAlumnoAdmin")
def actualizarAlumnoAdmin(
    idUsuario: int = Form(...),
    nombre: str = Form(...),
    correo: str = Form(...),
    rolId: int = Form(...),
    nivelId: int = Form(...),
    fechaInicio: date = Form(...),
    contrasenia: Optional[str] = Form(None),
    licId: Optional[int] = Form(None),
    fechaFin: Optional[date] = Form(None),
    foto: Optional[UploadFile] = File(None),
    usuario = Depends(require_admin),
    service=Depends(get_usuario_service)
):
    controller = UsuarioController(service)
    return controller.actualizarAlumnoAdmin(idUsuario= idUsuario,
                                       nombre= nombre,
                                       correo=correo,
                                       rolId=rolId,
                                       nivelId=nivelId,
                                       fechaInicio=fechaInicio,
                                       contrasenia=contrasenia,
                                       licId=licId,
                                       fechaFin=fechaFin,
                                       foto = foto)


@router.put("/eliminarUsuario")
def eliminarUsuario(
    request: UsuarioDeleteSchema,
    usuario = Depends(require_admin),
    service= Depends(get_usuario_service)
):
    controller = UsuarioController(service)

    return controller.eliminarUsuario(request) 


@router.put("/activar")
def activarUsuario(
    request: UsuarioDeleteSchema,
     usuario = Depends(require_admin),

    service= Depends(get_usuario_service)
):
    controller = UsuarioController(service)

    return controller.activarUsuario(request) 


@router.get("/listarUsuario")
def listarUsuario(
    usuario = Depends(require_admin),
    service = Depends(get_usuario_service)
):
    controller = UsuarioController(service)

    return controller.listarUsuario()

@router.get("/listarAlumno")
def listarAlumno(
    usuario = Depends(require_admin),
    service = Depends(get_usuario_service)
):
    controller = UsuarioController(service)

    return controller.listarAlumno()

@router.get("/busquedaAlumno")
def buscar_alumnos(
    nombre: Optional[str] = Query(None),
    correo: Optional[str] = Query(None),
    nivelId: Optional[int] =Query (None),
    licenciaturaId: Optional[int] = Query(None),
    estado: Optional[int] = Query(None),
    usuario = Depends(require_admin),
    service = Depends(get_usuario_service)
):
    controller = UsuarioController(service)
    return controller.filtrandoAlumno(nombre, correo, nivelId, licenciaturaId, estado)


@router.get("/busquedaUsuario")
def buscar_Usuario(
    nombre: Optional[str] = Query(None),
    correo: Optional[str] = Query(None),
    rol: Optional[int] =Query (None),
    estado: Optional[int] = Query (None),
    usuario = Depends(require_admin),
    service = Depends(get_usuario_service)
):
    controller = UsuarioController(service)
    return controller.filtrandoUsuario(nombre, correo, rol, estado)

@router.get("/obtnerUsuarioPorId")
def usuario(
    usuario = Depends(get_current_user),
    service = Depends(get_usuario_service)
):
    controller = UsuarioController(service)
    return controller.obtenerUsuarioPorId(usuario["idUsuario"])

@router.get("/obtnerAlumnoPorId")
def  alumno(
    usuario = Depends(get_current_user),
    service = Depends(get_usuario_service)
):
    controller = UsuarioController(service)
    return controller.obtenerAlumnorioPorId(usuario["idUsuario"])