from fastapi import APIRouter, Depends
from app.infrastructure.dependencies import get_nivel_service


from ..controller.nivelController import NivelController


nivel_router = APIRouter(prefix="/nivel", tags=["Nivel academico"])

@nivel_router.get("/listadoNivels")
def listadoNivel(
    service = Depends(get_nivel_service)
):
    
    controller = NivelController(service)
    return controller.obtenerNivel()