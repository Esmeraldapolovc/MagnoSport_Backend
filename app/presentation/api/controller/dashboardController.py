from fastapi import HTTPException
from datetime import date
from typing import Optional
from app.application.interfaces.service.IDashboardService import IDashboardService


class DashboardController:
    def __init__(self, service: IDashboardService):
        self.service = service

    # Métodos para día específico
    def asistenciaPorZonaAlDia(self, fecha: date = None):
        try:
            return self.service.asistenciaPorZonaAlDia(fecha)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def asistenciaPorHoraAlDia(self, fecha: date = None):
        try:
            return self.service.asistenciaPorHoraAlDia(fecha)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Métodos para mes completo
    def asistenciaPorZonaPorMes(self, fecha: date = None):
        try:
            return self.service.asistenciaPorZonaPorMes(fecha)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def asistenciaPorHoraPorMes(self, fecha: date = None):
        try:
            return self.service.asistenciaPorHoraPorMes(fecha)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Métodos para rango de fechas
    def asistenciaPorZonaYRangoFechas(self, fecha_inicio: date, fecha_fin: date):
        try:
            return self.service.asistenciaPorZonaYRangoFechas(fecha_inicio, fecha_fin)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def asistenciaPorHoraYRangoFechas(self, fecha_inicio: date, fecha_fin: date):
        try:
            return self.service.asistenciaPorHoraYRangoFechas(fecha_inicio, fecha_fin)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Estadísticas mensuales
    def obtenerEstadisticasMensuales(self, fecha: date = None):
        try:
            return self.service.obtenerEstadisticasMensuales(fecha)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

    def reservasAsistioPorZona(self, fecha: Optional[date] = None, es_mensual: bool = False):
        try:
            return self.service.reservasAsistioPorZona(fecha, es_mensual)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def reservasAsistioPorHora(self, fecha: Optional[date] = None, es_mensual: bool = False):
        try:
            return self.service.reservasAsistioPorHora(fecha, es_mensual)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))