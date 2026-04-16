from datetime import date

from fastapi import APIRouter, Depends

from app.presentation.schemas.reserva.reservaEquipoSchema import ReservaEquipoSchema
from ..controller.reservaController import ReservaController
from app.presentation.schemas.reserva import ReservaAlumno1Schemas, ReservaAdmin1Schemas, ReservaIdShemas, ReservaDeleteSchemas, EstadoUsoUpdateSchema
from app.infrastructure.dependencies import get_reserva_service, get_current_user

reserva_router = APIRouter(prefix="/reserva", tags=["Reserva"])

@reserva_router.post("/reservaUsuario1")
def reservaUsuario(
    request: ReservaAlumno1Schemas,
    usuario = Depends(get_current_user),
    service= Depends(get_reserva_service)
):
    controller = ReservaController(service)
    return  controller.reservaUsuario1(request, usuarioId=usuario["idUsuario"])



@reserva_router.post("/reservaUsuario2")
def reservaUsuario2(
    request: ReservaAdmin1Schemas,
    service= Depends(get_reserva_service)
):
    controller = ReservaController(service)
    return  controller.reservaUsuario2(request)



@reserva_router.get("/AgendaSemanaActual")
def  AgendaSemanaActual( 
    usuario = Depends(get_current_user),

    service = Depends(get_reserva_service)
):
    controller = ReservaController(service)
    return controller.obtenerAgendaSemanaActual(usuarioId=usuario["idUsuario"])

@reserva_router.put("/cancelarReserva")
def calcelarReserva(
    request: ReservaDeleteSchemas,
    usuario = Depends(get_current_user),
    service = Depends(get_reserva_service)
):
    controller = ReservaController(service)
    return controller.cancelarReserva(request, usuarioId=usuario["idUsuario"])

@reserva_router.get("/detalleReserva")
def  detalleReserva( 
    idReserva: int,
    service = Depends(get_reserva_service)
):
    controller = ReservaController(service)
    return controller.detalleReserva(idReserva)

@reserva_router.put("/estadoUso")
def registrarUsoEquipo(
    request: EstadoUsoUpdateSchema,
    service = Depends(get_reserva_service)
):
    
    controller = ReservaController(service)
    return controller.registrarUsoEquipo(request)

@reserva_router.get("/horario")
def  buscarHorario( 
    fecha: date,
    usuario = Depends(get_current_user),

    service = Depends(get_reserva_service)
):
    controller = ReservaController(service)
    return controller.buscarHorario(fecha, usuarioId=usuario["idUsuario"])

@reserva_router.post("/agregarEquipo")
def agregarEquipoAdicional(
    request: ReservaEquipoSchema,
    service = Depends(get_reserva_service)
):
    controller = ReservaController(service)
    return controller.agregarEquipoAdicional(request)