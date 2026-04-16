from sqlalchemy import func, extract, and_
from sqlalchemy.orm import Session
from app.application.interfaces.repository.IDashboardRepository import IDashboardRepository
from app.persistence.models.reserva import Reserva
from app.persistence.models.area import Area
from app.persistence.models.horario import Horario
from app.persistence.models.horarioDia import HorarioDia
from app.persistence.models.dia import Dia
from app.persistence.models.excepcionHorario import ExcepcionHorario
from datetime import date, datetime, timedelta
from typing import Optional, Tuple
from app.persistence.models.enums import EstadoReserva

class DashboardRepository(IDashboardRepository):

    def __init__(self, db: Session):
        self.db = db

    # ============= MÉTODOS PARA DÍA ESPECÍFICO =============

    def asistenciaPorZonaAlDia(self, fecha: Optional[date] = None) -> list[dict]:
        """Obtiene reservas por zona para un día específico"""
        fecha_consulta = fecha if fecha is not None else date.today()
        
        reservas_subq = self.db.query(
            Reserva.areaId,
            func.count(Reserva.idReserva).label('asistencia')
        ).filter(Reserva.fechaReserva == fecha_consulta)\
         .group_by(Reserva.areaId)\
         .subquery()
        
        resultados = self.db.query(
            Area.nombreArea.label('zona'),
            func.coalesce(reservas_subq.c.asistencia, 0).label('asistencia')
        ).outerjoin(reservas_subq, Area.idArea == reservas_subq.c.areaId).all()
        
        return [{"zona": r.zona, "asistencia": r.asistencia} for r in resultados]

    def asistenciaPorHoraAlDia(self, fecha: Optional[date] = None) -> list[dict]:
        """Obtiene reservas por hora para una fecha específica"""
        fecha_consulta = fecha if fecha is not None else date.today()
        
        resultados = self.db.query(
            func.DATE_FORMAT(Reserva.horaInicio, '%H:%i').label('hora'),
            func.count(Reserva.idReserva).label('asistencia')
        ).filter(
            Reserva.fechaReserva == fecha_consulta,
            func.HOUR(Reserva.horaInicio) >= 6,
            func.HOUR(Reserva.horaInicio) <= 18
        ).group_by(
            func.DATE_FORMAT(Reserva.horaInicio, '%H:%i')
        ).order_by(
            func.DATE_FORMAT(Reserva.horaInicio, '%H:%i')
        ).all()
        
        reservas_dict = {r.hora: r.asistencia for r in resultados}
        todas_las_horas = [f"{hora:02d}:00" for hora in range(6, 19)]
        
        return [
            {"hora": hora, "asistencia": reservas_dict.get(hora, 0)}
            for hora in todas_las_horas
        ]

    # ============= MÉTODOS PARA RANGO DE FECHAS =============

    def asistenciaPorZonaYRangoFechas(self, fecha_inicio: date, fecha_fin: date) -> list[dict]:
        """Obtiene reservas por zona para un rango de fechas personalizado"""
        print(f"Consultando reservas del {fecha_inicio} al {fecha_fin}")
        
        reservas_subq = self.db.query(
            Reserva.areaId,
            func.count(Reserva.idReserva).label('asistencia')
        ).filter(
            Reserva.fechaReserva >= fecha_inicio,
            Reserva.fechaReserva <= fecha_fin
        ).group_by(Reserva.areaId).subquery()
        
        resultados = self.db.query(
            Area.nombreArea.label('zona'),
            func.coalesce(reservas_subq.c.asistencia, 0).label('asistencia')
        ).outerjoin(reservas_subq, Area.idArea == reservas_subq.c.areaId).all()
        
        return [{"zona": r.zona, "asistencia": r.asistencia} for r in resultados]

    def asistenciaPorHoraYRangoFechas(self, fecha_inicio: date, fecha_fin: date) -> list[dict]:
        """Obtiene reservas por hora para un rango de fechas personalizado"""
        resultados = self.db.query(
            func.DATE_FORMAT(Reserva.horaInicio, '%H:%i').label('hora'),
            func.count(Reserva.idReserva).label('asistencia')
        ).filter(
            Reserva.fechaReserva >= fecha_inicio,
            Reserva.fechaReserva <= fecha_fin,
            func.HOUR(Reserva.horaInicio) >= 6,
            func.HOUR(Reserva.horaInicio) <= 18
        ).group_by(
            func.DATE_FORMAT(Reserva.horaInicio, '%H:%i')
        ).order_by(
            func.DATE_FORMAT(Reserva.horaInicio, '%H:%i')
        ).all()
        
        reservas_dict = {r.hora: r.asistencia for r in resultados}
        todas_las_horas = [f"{hora:02d}:00" for hora in range(6, 19)]
        
        return [
            {"hora": hora, "asistencia": reservas_dict.get(hora, 0)}
            for hora in todas_las_horas
        ]

    # ============= MÉTODOS PARA MES (con desglose por días de semana) =============

    def asistenciaPorZonaPorMes(self, fecha: Optional[date] = None) -> list[dict]:
        """
        Devuelve reservas por zona y por día de la semana (Lunes a Sábado)
        """
        fecha_consulta = fecha if fecha is not None else date.today()
        
        # Calcular primer y último día del mes
        primer_dia_mes = fecha_consulta.replace(day=1)
        if fecha_consulta.month == 12:
            ultimo_dia_mes = fecha_consulta.replace(year=fecha_consulta.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            ultimo_dia_mes = fecha_consulta.replace(month=fecha_consulta.month + 1, day=1) - timedelta(days=1)
        
        print(f"Consultando reservas del {primer_dia_mes} al {ultimo_dia_mes}")
        
        # Mapeo de días de la semana (1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes, 6=Sábado)
        dias_semana = {
            1: 'Lunes',
            2: 'Martes', 
            3: 'Miércoles',
            4: 'Jueves',
            5: 'Viernes',
            6: 'Sábado'
        }
        
        resultados = []
        
        # Para cada zona, obtener las reservas por día de la semana
        zonas = self.db.query(Area.idArea, Area.nombreArea).all()
        
        for zona in zonas:
            zona_data = {
                "zona": zona.nombreArea,
                "dias": {}
            }
            
            for dia_num, dia_nombre in dias_semana.items():
                # Contar reservas para esta zona y este día de la semana en el mes
                # DAYOFWEEK en MySQL: 1=Domingo, 2=Lunes, 3=Martes, 4=Miércoles, 5=Jueves, 6=Viernes, 7=Sábado
                total = self.db.query(func.count(Reserva.idReserva)).filter(
                    Reserva.areaId == zona.idArea,
                    Reserva.fechaReserva >= primer_dia_mes,
                    Reserva.fechaReserva <= ultimo_dia_mes,
                    func.DAYOFWEEK(Reserva.fechaReserva) == dia_num + 1
                ).scalar() or 0
                
                zona_data["dias"][dia_nombre] = total
            
            # Calcular total del mes para esta zona
            zona_data["total_mes"] = sum(zona_data["dias"].values())
            resultados.append(zona_data)
        
        return resultados

    def asistenciaPorHoraPorMes(self, fecha: Optional[date] = None) -> list[dict]:
   
     fecha_consulta = fecha if fecha is not None else date.today()
    
    # Calcular primer y último día del mes
     primer_dia_mes = fecha_consulta.replace(day=1)
     if fecha_consulta.month == 12:
        ultimo_dia_mes = fecha_consulta.replace(year=fecha_consulta.year + 1, month=1, day=1) - timedelta(days=1)
     else:
        ultimo_dia_mes = fecha_consulta.replace(month=fecha_consulta.month + 1, day=1) - timedelta(days=1)
    
     print(f"Consultando reservas por hora del {primer_dia_mes} al {ultimo_dia_mes}")
    
    # Mapeo de días de la semana (para MySQL: 2=Lunes, 3=Martes, 4=Miércoles, 5=Jueves, 6=Viernes, 7=Sábado)
     dias_semana = {
        2: 'Lunes',
        3: 'Martes', 
        4: 'Miércoles',
        5: 'Jueves',
        6: 'Viernes',
        7: 'Sábado'
    }
    
    # Generar todas las horas posibles
     todas_las_horas = [f"{hora:02d}:00" for hora in range(6, 19)]
    
    # Inicializar estructura de resultados
     resultados_dict = {}
     for hora in todas_las_horas:
        resultados_dict[hora] = {
            "hora": hora,
            "total": 0,
            "dias": {
                "Lunes": 0,
                "Martes": 0,
                "Miércoles": 0,
                "Jueves": 0,
                "Viernes": 0,
                "Sábado": 0
            }
        }
    
    # Consulta para obtener reservas por hora y día de la semana
     for dia_num, dia_nombre in dias_semana.items():
        for hora in todas_las_horas:
            # Extraer la hora (sin minutos)
            hora_num = int(hora.split(':')[0])
            
            total = self.db.query(func.count(Reserva.idReserva)).filter(
                Reserva.fechaReserva >= primer_dia_mes,
                Reserva.fechaReserva <= ultimo_dia_mes,
                func.HOUR(Reserva.horaInicio) == hora_num,
                func.HOUR(Reserva.horaInicio) >= 6,
                func.HOUR(Reserva.horaInicio) <= 18,
                func.DAYOFWEEK(Reserva.fechaReserva) == dia_num
            ).scalar() or 0
            
            resultados_dict[hora]["dias"][dia_nombre] = total
            resultados_dict[hora]["total"] += total
    
    # Convertir a lista
     return list(resultados_dict.values())

    # ============= MÉTODOS PARA ASISTENCIAS (estado ASISTIO) =============

    def reservasAsistioPorZona(self, fecha: Optional[date] = None, es_mensual: bool = False) -> list[dict]:
        """
        Devuelve asistencias por zona
        - Si es_mensual = False: devuelve total del día específico
        - Si es_mensual = True: devuelve desglose por días de la semana (Lunes a Sábado)
        """
        fecha_consulta = fecha if fecha is not None else date.today()
        
        # Si NO es mensual, comportamiento original (día específico)
        if not es_mensual:
            reservas_subq = self.db.query(
                Reserva.areaId,
                func.count(Reserva.idReserva).label('asistio')
            ).filter(
                Reserva.fechaReserva == fecha_consulta,
                Reserva.estado == EstadoReserva.ASISTIO
            ).group_by(Reserva.areaId).subquery()
            
            resultados = self.db.query(
                Area.nombreArea.label('zona'),
                func.coalesce(reservas_subq.c.asistio, 0).label('asistio')
            ).outerjoin(reservas_subq, Area.idArea == reservas_subq.c.areaId).all()
            
            return [{"zona": r.zona, "asistio": r.asistio} for r in resultados]
        
        # Si ES mensual, devolver desglose por días de la semana
        # Calcular primer y último día del mes
        primer_dia_mes = fecha_consulta.replace(day=1)
        if fecha_consulta.month == 12:
            ultimo_dia_mes = fecha_consulta.replace(year=fecha_consulta.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            ultimo_dia_mes = fecha_consulta.replace(month=fecha_consulta.month + 1, day=1) - timedelta(days=1)
        
        print(f"Consultando asistencias del {primer_dia_mes} al {ultimo_dia_mes}")
        
        # Mapeo de días de la semana
        dias_semana = {
            1: 'Lunes',
            2: 'Martes', 
            3: 'Miércoles',
            4: 'Jueves',
            5: 'Viernes',
            6: 'Sábado'
        }
        
        resultados = []
        
        # Para cada zona, obtener las asistencias por día de la semana
        zonas = self.db.query(Area.idArea, Area.nombreArea).all()
        
        for zona in zonas:
            zona_data = {
                "zona": zona.nombreArea,
                "dias": {}
            }
            
            for dia_num, dia_nombre in dias_semana.items():
                # Contar asistencias para esta zona y este día de la semana en el mes
                total = self.db.query(func.count(Reserva.idReserva)).filter(
                    Reserva.areaId == zona.idArea,
                    Reserva.fechaReserva >= primer_dia_mes,
                    Reserva.fechaReserva <= ultimo_dia_mes,
                    Reserva.estado == EstadoReserva.ASISTIO,
                    func.DAYOFWEEK(Reserva.fechaReserva) == dia_num + 1
                ).scalar() or 0
                
                zona_data["dias"][dia_nombre] = total
            
            # Calcular total del mes para esta zona
            zona_data["total_mes"] = sum(zona_data["dias"].values())
            resultados.append(zona_data)
        
        return resultados

    def reservasAsistioPorHora(self, fecha: Optional[date] = None, es_mensual: bool = False) -> list[dict]:
        """
        Obtiene asistencias por hora
        - Si es_mensual = False: devuelve por hora del día específico
        - Si es_mensual = True: devuelve acumulado por hora del mes
        """
        fecha_consulta = fecha if fecha is not None else date.today()
        
        if es_mensual:
            # Calcular primer y último día del mes
            primer_dia_mes = fecha_consulta.replace(day=1)
            if fecha_consulta.month == 12:
                ultimo_dia_mes = fecha_consulta.replace(year=fecha_consulta.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                ultimo_dia_mes = fecha_consulta.replace(month=fecha_consulta.month + 1, day=1) - timedelta(days=1)
            
            print(f"Consultando asistencias por hora del {primer_dia_mes} al {ultimo_dia_mes}")
            
            resultados = self.db.query(
                func.DATE_FORMAT(Reserva.horaInicio, '%H:%i').label('hora'),
                func.count(Reserva.idReserva).label('asistio')
            ).filter(
                Reserva.fechaReserva >= primer_dia_mes,
                Reserva.fechaReserva <= ultimo_dia_mes,
                Reserva.estado == EstadoReserva.ASISTIO,
                func.HOUR(Reserva.horaInicio) >= 6,
                func.HOUR(Reserva.horaInicio) <= 18
            ).group_by(
                func.DATE_FORMAT(Reserva.horaInicio, '%H:%i')
            ).order_by(
                func.DATE_FORMAT(Reserva.horaInicio, '%H:%i')
            ).all()
        else:
            # Día específico
            resultados = self.db.query(
                func.DATE_FORMAT(Reserva.horaInicio, '%H:%i').label('hora'),
                func.count(Reserva.idReserva).label('asistio')
            ).filter(
                Reserva.fechaReserva == fecha_consulta,
                Reserva.estado == EstadoReserva.ASISTIO,
                func.HOUR(Reserva.horaInicio) >= 6,
                func.HOUR(Reserva.horaInicio) <= 18
            ).group_by(
                func.DATE_FORMAT(Reserva.horaInicio, '%H:%i')
            ).order_by(
                func.DATE_FORMAT(Reserva.horaInicio, '%H:%i')
            ).all()
        
        reservas_dict = {r.hora: r.asistio for r in resultados}
        todas_las_horas = [f"{hora:02d}:00" for hora in range(6, 19)]
        
        return [
            {"hora": hora, "asistio": reservas_dict.get(hora, 0)}
            for hora in todas_las_horas
        ]

    # ============= ESTADÍSTICAS MENSUALES =============

    def obtenerEstadisticasMensuales(self, fecha: Optional[date] = None) -> dict:
        """Obtiene estadísticas completas del mes"""
        fecha_consulta = fecha if fecha is not None else date.today()
        
        # Calcular primer y último día del mes
        primer_dia_mes = fecha_consulta.replace(day=1)
        if fecha_consulta.month == 12:
            ultimo_dia_mes = fecha_consulta.replace(year=fecha_consulta.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            ultimo_dia_mes = fecha_consulta.replace(month=fecha_consulta.month + 1, day=1) - timedelta(days=1)
        
        # Total de reservas en el mes
        total_reservas = self.db.query(func.count(Reserva.idReserva)).filter(
            Reserva.fechaReserva >= primer_dia_mes,
            Reserva.fechaReserva <= ultimo_dia_mes
        ).scalar() or 0
        
        # Días con actividad
        dias_activos = self.db.query(func.count(func.distinct(Reserva.fechaReserva))).filter(
            Reserva.fechaReserva >= primer_dia_mes,
            Reserva.fechaReserva <= ultimo_dia_mes
        ).scalar() or 0
        
        # Promedio de reservas por día
        promedio_diario = total_reservas / dias_activos if dias_activos > 0 else 0
        
        # Zona más popular del mes
        zona_top = self.db.query(
            Area.nombreArea,
            func.count(Reserva.idReserva).label('total')
        ).join(Reserva, Area.idArea == Reserva.areaId)\
         .filter(
            Reserva.fechaReserva >= primer_dia_mes,
            Reserva.fechaReserva <= ultimo_dia_mes
        ).group_by(Area.idArea)\
         .order_by(func.count(Reserva.idReserva).desc())\
         .first()
        
        return {
            "total_reservas": total_reservas,
            "dias_activos": dias_activos,
            "promedio_diario": round(promedio_diario, 2),
            "zona_mas_popular": zona_top[0] if zona_top else "Ninguna",
            "reservas_zona_top": zona_top[1] if zona_top else 0,
            "mes": fecha_consulta.strftime("%B %Y"),
            "primer_dia": primer_dia_mes,
            "ultimo_dia": ultimo_dia_mes
        }