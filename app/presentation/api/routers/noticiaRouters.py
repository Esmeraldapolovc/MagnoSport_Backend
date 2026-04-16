from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Form, Query

from app.presentation.schemas.noticias.eliminarNoticiaSchema import EliminarNoticiaSchema
from ..controller.noticiaController import NoticiaController
from app.presentation.schemas.noticias import AgregarNoticiaSchema, ActualizarNoticiaSchema
from app.infrastructure.dependencies import get_Noticia_service

noticia_router = APIRouter(prefix="/noticia", tags=["Noticia"])

@noticia_router.post("/agregarNoticia")
def agregarNoticia(
    request: AgregarNoticiaSchema,
    service = Depends(get_Noticia_service)
):
    controller = NoticiaController(service)
    return controller.agregarNoticia(request)

@noticia_router.get("/obtenerNoticias")
def obtenerNoticias(
    service = Depends(get_Noticia_service)
):
    controller = NoticiaController(service)
    return controller.obtenerNoticias()


@noticia_router.get("/detalleNoticia")
def detalleNoticia(
    idNoticia: int= Query(...),
    service = Depends(get_Noticia_service)
):
    controller = NoticiaController(service)
    return controller.detalleNoticia(idNoticia)

@noticia_router.put("/modificarNoticia")
def modificarNoticia(
    request: ActualizarNoticiaSchema,
    service = Depends(get_Noticia_service)
):
    controller = NoticiaController(service)
    return controller.modificarNoticia(request)


@noticia_router.patch("/eliminarNoticia")
def eliminarNoticia(
    request: EliminarNoticiaSchema,
    service = Depends(get_Noticia_service)
):
    controller = NoticiaController(service)
    return controller.eliminarNoticia(request)


@noticia_router.get("/buscarPorFecha")
def buscarPorFecha(
    fecha: date = Query(...),
    service = Depends(get_Noticia_service)
):
    controller = NoticiaController(service)
    return controller.buscarPorFecha(fecha)
