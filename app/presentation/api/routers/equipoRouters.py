from fastapi import APIRouter, Depends, Form, Query
from app.presentation.schemas.equipo import AgregarEquipoSchema, ActualizarEquipoSchema
from ..controller.equipoController import EquipoController
from app.infrastructure.dependencies import get_equipo_service

equipo_router = APIRouter(prefix="/equipo", tags=["Equipo"])

@equipo_router.post("/registrarEquipo")
def registrarEquipo(
    request: AgregarEquipoSchema,
    service = Depends(get_equipo_service)
):
    controller = EquipoController(service)
    return controller.registrarEquipo(request)


@equipo_router.put("/actualizarEquipo")
def actualizarEquipo(
    request: ActualizarEquipoSchema,
    service = Depends(get_equipo_service)
):
    controller = EquipoController(service)
    return controller.actualizarEquipo(request)


@equipo_router.get("/ListadoEquipos")
def ListadoEquipos(
    service = Depends(get_equipo_service)
):
    controller = EquipoController(service)
    return controller.ListadoEquipos()

@equipo_router.get("/obtenerEquipoPorNombre")
def obtenerEquipoPorNombre(
    nombre: str = Query(..., description="Nombre del equipo a buscar"),
    service = Depends(get_equipo_service)
):
    controller = EquipoController(service)
    return controller.obtenerEquipoPorNombre(nombre)

@equipo_router.get("/obtenerEquipoPorId")
def obtenerEquipoPorId(
    idEquipo: int = Query(..., description="ID del equipo a buscar"),
    service = Depends(get_equipo_service)
):
    controller = EquipoController(service)
    return controller.obtenerEquipoPorId(idEquipo)

@equipo_router.get("/obtenerEquipoGeneralPorNombre")
def obtenerEquipoGeneralPorNombre(
    nombre: str = Query(..., description="Nombre del equipo a buscar"),
    service = Depends(get_equipo_service)
):
    controller = EquipoController(service)
    return controller.obtenerEquipoGeneralPorNombre(nombre)