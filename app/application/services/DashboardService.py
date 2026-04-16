from datetime import date
from typing import Optional
from ..interfaces.repository.IDashboardRepository import IDashboardRepository
from ..interfaces.service.IDashboardService import IDashboardService


class DashboardService(IDashboardService):

    def __init__(self, dashboard_repository: IDashboardRepository):
        self.dashboard_repository = dashboard_repository

    # Métodos para día específico
    def asistenciaPorZonaAlDia(self, fecha: date = None) -> list[dict]:
        return self.dashboard_repository.asistenciaPorZonaAlDia(fecha)

    def asistenciaPorHoraAlDia(self, fecha: date = None) -> list[dict]:
        return self.dashboard_repository.asistenciaPorHoraAlDia(fecha)

    # Métodos para mes completo
    def asistenciaPorZonaPorMes(self, fecha: date = None) -> list[dict]:
        return self.dashboard_repository.asistenciaPorZonaPorMes(fecha)

    def asistenciaPorHoraPorMes(self, fecha: date = None) -> list[dict]:
        return self.dashboard_repository.asistenciaPorHoraPorMes(fecha)

    # Métodos para rango de fechas personalizado
    def asistenciaPorZonaYRangoFechas(self, fecha_inicio: date, fecha_fin: date) -> list[dict]:
        if fecha_inicio > fecha_fin:
            raise ValueError("La fecha de inicio no puede ser mayor a la fecha de fin")
        return self.dashboard_repository.asistenciaPorZonaYRangoFechas(fecha_inicio, fecha_fin)

    def asistenciaPorHoraYRangoFechas(self, fecha_inicio: date, fecha_fin: date) -> list[dict]:
        if fecha_inicio > fecha_fin:
            raise ValueError("La fecha de inicio no puede ser mayor a la fecha de fin")
        return self.dashboard_repository.asistenciaPorHoraYRangoFechas(fecha_inicio, fecha_fin)

    # Estadísticas mensuales
    def obtenerEstadisticasMensuales(self, fecha: date = None) -> dict:
        return self.dashboard_repository.obtenerEstadisticasMensuales(fecha)
    
    def reservasAsistioPorZona(self, fecha: Optional[date] = None, es_mensual: bool = False) -> list[dict]:
        return self.dashboard_repository.reservasAsistioPorZona(fecha, es_mensual)
    
    def reservasAsistioPorHora(self, fecha: Optional[date] = None, es_mensual: bool = False) -> list[dict]:
        return self.dashboard_repository.reservasAsistioPorHora(fecha, es_mensual)