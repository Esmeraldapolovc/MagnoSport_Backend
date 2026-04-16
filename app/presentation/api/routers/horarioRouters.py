from fastapi import APIRouter, Depends
from typing import Optional
from ..controller.horarioController import HorarioController
from app.presentation.schemas.HorarioSchemas import HorarioCreateSchema, ExcepcionSchema
from app.infrastructure.dependencies import get_horario_service, get_current_user, require_admin
from datetime import date

horario_router = APIRouter(prefix="/horario", tags=["Horario"])
 

@horario_router.post("/registrarHorario")
def crearHorario(
    request: HorarioCreateSchema,
    usuario = Depends(require_admin),

    service=Depends(get_horario_service)

):
    controller = HorarioController(service)
    return controller.crearHorario(request)

@horario_router.get("/listadoHorario")
def listadoHorario(
     usuario = Depends(require_admin),

    serivece = Depends(get_horario_service)
):
    controller = HorarioController(serivece)
    return controller.listarHorarios()

@horario_router.post("/crearExcepcion")
def crearExcepcion(
    request: ExcepcionSchema,
    usuario = Depends(require_admin),

    service = Depends(get_horario_service)
):
    controller = HorarioController(service)
    return controller.crearExcepcion(request)

@horario_router.get("/buscar")
def buscar_por_fecha(fecha: date, 
                         usuario = Depends(require_admin),

                     service=Depends(get_horario_service)):
   
    controller = HorarioController(service)
    
    return controller.consultarFecha(fecha)

