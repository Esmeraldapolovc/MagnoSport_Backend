from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, List, Dict

class IDashboardRepository(ABC):

    @abstractmethod
    def asistenciaPorZonaAlDia(self, fecha: Optional[date] = None) -> list[dict]:
        """Reservas por zona para un día específico"""
        pass

    @abstractmethod
    def asistenciaPorZonaPorMes(self, fecha: Optional[date] = None) -> list[dict]:
        """Reservas por zona para todo el mes"""
        pass

    @abstractmethod
    def asistenciaPorHoraAlDia(self, fecha: Optional[date] = None) -> list[dict]:
        """Reservas por hora para un día específico"""
        pass

    @abstractmethod
    def asistenciaPorHoraPorMes(self, fecha: Optional[date] = None) -> list[dict]:
        """Reservas por hora para todo el mes (acumulado)"""
        pass

    @abstractmethod
    def asistenciaPorZonaYRangoFechas(self, fecha_inicio: date, fecha_fin: date) -> list[dict]:
        """Reservas por zona para un rango de fechas"""
        pass

    @abstractmethod
    def asistenciaPorHoraYRangoFechas(self, fecha_inicio: date, fecha_fin: date) -> list[dict]:
        """Reservas por hora para un rango de fechas"""
        pass

    @abstractmethod
    def obtenerEstadisticasMensuales(self, fecha: Optional[date] = None) -> dict:
        """Estadísticas completas del mes"""
        pass

    @abstractmethod
    def reservasAsistioPorZona(self, fecha: Optional[date] = None, es_mensual: bool = False) -> list[dict]:
        """Obtiene reservas con estado ASISTIO por zona (día o mes)"""
        pass

    @abstractmethod
    def reservasAsistioPorHora(self, fecha: Optional[date] = None, es_mensual: bool = False) -> list[dict]:
        """Obtiene reservas con estado ASISTIO por hora (día o mes)"""
        pass