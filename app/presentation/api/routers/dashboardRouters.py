from datetime import date
from fastapi import APIRouter, Depends
from app.presentation.api.controller.dashboardController import DashboardController
from app.infrastructure.dependencies import get_dashboard_service

asistencia_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@asistencia_router.get("/asistenciaPorZonaAlDIa")
def asistencia_por_zona_al_dia(
    fecha: date = None,
    service = Depends(get_dashboard_service)):


    controller = DashboardController(service)
    return controller.asistenciaPorZonaAlDia(fecha)

@asistencia_router.get("/asistenciaPorHoraAlDIa")
def asistencia_por_hora_al_dia(
    fecha: date = None,
      service = Depends(get_dashboard_service)):
    
    controller = DashboardController(service)
    return controller.asistenciaPorHoraAlDia(fecha) 

@asistencia_router.get("/asistenciaPorZonaPorMes")
def asistencia_por_zona_por_mes(
    fecha: date = None,
      service = Depends(get_dashboard_service)):
    
    controller = DashboardController(service)
    return controller.asistenciaPorZonaPorMes(fecha)

@asistencia_router.get("/asistenciaPorHoraPorMes")
def asistencia_por_hora_por_mes(
    fecha: date = None,
      service = Depends(get_dashboard_service)):
    
    controller = DashboardController(service)
    return controller.asistenciaPorHoraPorMes(fecha)

@asistencia_router.get("/asistenciaPorZonaYRangoFechas")
def asistencia_por_zona_rango_fechas(
    fecha_inicio: date,
    fecha_fin: date,
      service = Depends(get_dashboard_service)):
    
    controller = DashboardController(service)
    return controller.asistenciaPorZonaYRangoFechas(fecha_inicio, fecha_fin)

@asistencia_router.get("/asistenciaPorHoraYRangoFechas")
def asistencia_por_hora_rango_fechas(
    fecha_inicio: date,
    fecha_fin: date,
      service = Depends(get_dashboard_service)):
    
    controller = DashboardController(service)
    return controller.asistenciaPorHoraYRangoFechas(fecha_inicio, fecha_fin)

@asistencia_router.get("/obtenerEstadisticasMensuales")
def obtener_estadisticas_mensuales(
    fecha: date = None,
      service = Depends(get_dashboard_service)):
    
    controller = DashboardController(service)
    return controller.obtenerEstadisticasMensuales(fecha)

@asistencia_router.get("/reservasAsistioPorZona")
def reservas_asistio_por_zona(
    fecha: date = None,
    es_mensual: bool = False,
      service = Depends(get_dashboard_service)):
    
    controller = DashboardController(service)
    return controller.reservasAsistioPorZona(fecha, es_mensual) 

@asistencia_router.get("/reservasAsistioPorHora")
def reservas_asistio_por_hora(  
    fecha: date = None,
    es_mensual: bool = False,
      service = Depends(get_dashboard_service)):
    
    controller = DashboardController(service)
    return controller.reservasAsistioPorHora(fecha, es_mensual)