from datetime import date

from fastapi import APIRouter, Depends

from app.presentation.schemas.reserva.messageResponse import AsistenciaExitoSchema
from ..controller.aistenciasyReservasController import AsistenciasyReservasController
from app.infrastructure.dependencies import get_asistenciasyreservas_service

asistenciasyreservas_router = APIRouter(prefix="/asistenciasyreservas", tags=["Asistencias y Reservas"])

@asistenciasyreservas_router.get("/AsistenciasyReservas")
def obtenerHorariosAsistenciasyReservas(idArea: int, 
    service = Depends(get_asistenciasyreservas_service)
    ):

    controller = AsistenciasyReservasController(service)
    return controller.obtenerHorariosAsistenciasyReservas(idArea)

@asistenciasyreservas_router.get("/AsistenciasyReservasPorFecha")
def obtenerHorariosAsistenciasyReservasPorFecha(fecha_referencia: date, idArea: int,
    service = Depends(get_asistenciasyreservas_service)
    ):

    controller = AsistenciasyReservasController(service)
    return controller.obtenerHorariosAsistenciasyReservasPorFecha(fecha_referencia, idArea)



@asistenciasyreservas_router.get("/detallesusuarioReserva")
def obtenerdetallesusuario(idReserva: int,
    service = Depends(get_asistenciasyreservas_service)
    ):

    controller = AsistenciasyReservasController(service)
    return controller.obtenerdetallesusuario(idReserva)


@asistenciasyreservas_router.patch("/asistencia", response_model=AsistenciaExitoSchema)
def registrar_asistencia(
    idReserva: int,
    service = Depends(get_asistenciasyreservas_service)):
   
    controller = AsistenciasyReservasController(service)
    return controller.registrarAsistencia(idReserva)
     