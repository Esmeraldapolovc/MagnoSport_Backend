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
        pass

    @abstractmethod
    def asistenciaPorHoraPorMes(self, fecha: Optional[date] = None) -> list[dict]:
        pass

    @abstractmethod
    def asistenciaPorZonaYRangoFechas(self, fecha_inicio: date, fecha_fin: date) -> list[dict]:
        pass

    @abstractmethod
    def asistenciaPorHoraYRangoFechas(self, fecha_inicio: date, fecha_fin: date) -> list[dict]:
        pass

    @abstractmethod
    def obtenerEstadisticasMensuales(self, fecha: Optional[date] = None) -> dict:
        pass

    @abstractmethod
    def reservasAsistioPorZona(self, fecha: Optional[date] = None, es_mensual: bool = False) -> list[dict]:
        pass

    @abstractmethod
    def reservasAsistioPorHora(self, fecha: Optional[date] = None, es_mensual: bool = False) -> list[dict]:
        pass