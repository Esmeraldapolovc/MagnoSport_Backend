from fastapi import APIRouter, Depends, Form, Query
from app.infrastructure.dependencies import get_licenciatura_service
from ..controller.licenciaturaController import LicenciaturaController


licenciatura_router = APIRouter(prefix="/licenciatura", tags=["Licenciatura"])


@licenciatura_router.get("/obtenerLicenciaturas")
def obtenerLicenciaturas(
    service = Depends(get_licenciatura_service)
):
    controller = LicenciaturaController(service)
    return controller.obtenerLicenciatura()