from app.domain.entities.horario import Horario as HorarioEntidad
from app.domain.entities.horario import Estado
from app.domain.entities import ExcepcionHorario
from ..interfaces.service.IHorarioService import IHorarioService
from ..interfaces.repository.IHorarioRepository import IHorarioRepository
from ..dtos.horario import HorarioCreateDTO, ExcepcionCreateDTO
from typing import List
from datetime import date, timedelta, datetime

class HorarioService(IHorarioService):
    def __init__(self, repository: IHorarioRepository):
        self.repository = repository

    def crearHorario(self, dto: HorarioCreateDTO) -> str:
        dias_a_registrar = dto.dias
        
        if not dias_a_registrar or len(dias_a_registrar) == 0:
            dias_a_registrar = self._calcular_dias_en_rango(dto.fechaInicio, dto.fechaFin)

        choque = self.repository.verificarSolapamiento(
            dto.fechaInicio, dto.fechaFin, 
            dto.horaInicio, dto.horaFin, 
            dias_a_registrar
        )
    
        if choque:
            raise ValueError("El horario se solapa con uno ya existente en esos días y horas.")
            
        nueva_entidad = HorarioEntidad(
            fechaInicio=dto.fechaInicio,
            fechaFin=dto.fechaFin,
            horaInicio=dto.horaInicio,
            horaFin=dto.horaFin,
            estado=dto.estado
        )

        self.repository.crearHorario(nueva_entidad, dias_a_registrar)
        return "Horario registrado exitosamente."

    def _calcular_dias_en_rango(self, inicio, fin) -> list:
        """ Método privado para obtener IDs únicos de días entre dos fechas """
        dias_encontrados = set()
        fecha_actual = inicio
        
        while fecha_actual <= fin:
            id_dia = fecha_actual.weekday() + 1
            dias_encontrados.add(id_dia)
            
            if len(dias_encontrados) == 7:
                break
                
            fecha_actual += timedelta(days=1)
            
        return list(dias_encontrados)

    def listarHorarios(self) -> List[dict]:
     horarios_db = self.repository.listarHorarios()
    
     # Configurar el rango de la semana actual (Lunes a Sábado)
     hoy = date.today()
     lunes_actual = hoy - timedelta(days=hoy.weekday())
    
     dias_nombres_map = {1: "Lunes", 2: "Martes", 3: "Miércoles", 4: "Jueves", 5: "Viernes", 6: "Sábado"}
     resultado_semanal = []

    # Iterar del día 1 (Lunes) al 6 (Sábado)
     for i in range(1, 7):
        fecha_evaluar = lunes_actual + timedelta(days=i-1)
        dia_nombre = dias_nombres_map[i]
        
        bloques_del_dia = []
        horarios_ids_del_dia = []
        
        # Generar bloques horarios de 1 hora entre 06:00 y 19:00
        hora_inicio_gen = datetime.combine(fecha_evaluar, datetime.strptime("06:00", "%H:%M").time())
        hora_fin_gen = datetime.combine(fecha_evaluar, datetime.strptime("19:00", "%H:%M").time())
        
        iterador_hora = hora_inicio_gen
        
        while iterador_hora < hora_fin_gen:
            t_ini = iterador_hora.time()
            dt_fin = iterador_hora + timedelta(hours=1)
            t_fin = dt_fin.time()

            # --- Lógica de búsqueda de horario real ---
            horario_encontrado = None
            
            # Buscar en TODOS los horarios para esta hora específica
            for h in horarios_db:
                dias_permitidos_ids = [d.idDia for d in h.dias]
                if h.fechaInicio <= fecha_evaluar <= h.fechaFin and i in dias_permitidos_ids:
                    if h.horaInicio <= t_ini < h.horaFin:
                        horario_encontrado = h
                        if h.idHorario not in horarios_ids_del_dia:
                            horarios_ids_del_dia.append(h.idHorario)
                        break
            
            # --- Construcción del bloque ---
            tramo_nombre = "Sin horario"
            estado_bloque = "Sin horario asignado"
            es_exce = False
            horario_id_bloque = None

            if horario_encontrado:
                horario_id_bloque = horario_encontrado.idHorario
                estado_bloque = horario_encontrado.estado.value if hasattr(horario_encontrado.estado, 'value') else horario_encontrado.estado
                tramo_nombre = "Regular"
                
                # IMPORTANTE: Ordenar excepciones por ID descendente para tomar la más reciente
                excepciones_ordenadas = sorted(
                    horario_encontrado.excepciones,
                    key=lambda ex: ex.idExcepcion,
                    reverse=True  # La más reciente primero (ID más alto)
                )
                
                # Buscar la PRIMERA excepción que aplique (la más reciente)
                for excepcion in excepciones_ordenadas:
                    if (excepcion.fechaInicio <= fecha_evaluar <= excepcion.fechaFin
                        and excepcion.horaInicio <= t_ini < excepcion.horaFin):
                        estado_bloque = excepcion.estado.value if hasattr(excepcion.estado, 'value') else excepcion.estado
                        tramo_nombre = "Excepción"
                        es_exce = True
                        break  # Usar la primera que encontramos (la más reciente)
            
            bloques_del_dia.append({
                "tramo": tramo_nombre,
                "horaInicio": t_ini.strftime("%H:%M"),
                "horaFin": t_fin.strftime("%H:%M"),
                "estado": estado_bloque,
                "esExcepcion": es_exce,
                "horarioId": horario_id_bloque
            })
            
            iterador_hora = dt_fin

        resultado_semanal.append({
            "id": horarios_ids_del_dia[0] if horarios_ids_del_dia else None,
            "ids": horarios_ids_del_dia,
            "fecha": fecha_evaluar.isoformat(),
            "diaNombre": dia_nombre,
            "bloques": bloques_del_dia
        })

     return resultado_semanal

    def crearExcepcion(self, dto: ExcepcionCreateDTO) -> dict:
        horario_base = self.repository.obtenerPorId(dto.horarioId)
        if not horario_base:
            raise ValueError("El horario que intenta modificar no existe.")
        
        mensaje_ajuste = None
        fecha_inicio_original = dto.fechaInicio
        fecha_fin_original = dto.fechaFin
        
        # Ajustar fechas si es necesario
        fecha_inicio_ajustada = dto.fechaInicio
        fecha_fin_ajustada = dto.fechaFin
        
        # Validar que la fecha de inicio no sea menor que la fecha de inicio del horario base
        if dto.fechaInicio < horario_base.fechaInicio:
            fecha_inicio_ajustada = horario_base.fechaInicio
            mensaje_ajuste = f"La fecha de inicio se ajustó a {horario_base.fechaInicio} (límite del horario base)"
        
        # Validar que la fecha de fin no sea mayor que la fecha de fin del horario base
        if dto.fechaFin > horario_base.fechaFin:
            fecha_fin_ajustada = horario_base.fechaFin
            mensaje_ajuste = f"La fecha de fin se ajustó a {horario_base.fechaFin} (límite del horario base)" if not mensaje_ajuste else f"{mensaje_ajuste} y la fecha de fin se ajustó a {horario_base.fechaFin}"
        
        # Validar que la fecha de inicio no sea mayor que la fecha de fin después de ajustes
        if fecha_inicio_ajustada > fecha_fin_ajustada:
            raise ValueError("El rango de fechas ajustado no es válido: la fecha de inicio es posterior a la fecha de fin")
        
        # Crear la excepción con las fechas ajustadas
        nueva_excepcion = ExcepcionHorario(
            horario=dto.horarioId,
            fechaInicio=fecha_inicio_ajustada,
            fechaFin=fecha_fin_ajustada,
            horaInicio=dto.horaInicio,
            horaFin=dto.horaFin,
            estado=dto.estado
        )
        
        self.repository.crearExcepcion(nueva_excepcion)
        
        # Preparar respuesta con mensaje
        respuesta = {
            "excepcion": nueva_excepcion,
            "mensaje": f"Modificación horaria registrada del {fecha_inicio_ajustada} al {fecha_fin_ajustada}."
        }
        
        if mensaje_ajuste:
            respuesta["mensaje_adicional"] = mensaje_ajuste
            respuesta["fechas_originales"] = {
                "fechaInicio": fecha_inicio_original,
                "fechaFin": fecha_fin_original
            }
        
        return respuesta

    def obtenerEstadoPorFecha(self, fecha_inicial: date):
     lunes_semana = fecha_inicial - timedelta(days=fecha_inicial.weekday())
    
     resultado_agenda = []
     HORA_APERTURA = 6
     HORA_CIERRE = 19

     for i in range(1, 7):  # De Lunes (1) a Sábado (6)
        fecha_consulta = lunes_semana + timedelta(days=i-1)
        
        # Buscar TODOS los horarios para esta fecha
        horarios = self.repository.buscarPorFecha(fecha_consulta)
        
        bloques_del_dia = []
        horarios_ids = []
        
        # Iteramos hora por hora
        for hora in range(HORA_APERTURA, HORA_CIERRE):
            t_ini = datetime.strptime(f"{hora}:00", "%H:%M").time()
            t_fin = datetime.strptime(f"{hora + 1}:00", "%H:%M").time()
            
            # Valores por defecto para "Sin horario"
            tramo_nombre = "Sin horario"
            estado_bloque = "Sin horario asignado"
            es_exce = False
            horario_id_bloque = None
            
            # Buscar en TODOS los horarios disponibles
            for horario in horarios:
                # Verificar si la hora actual cae dentro del rango de este horario
                if horario.horaInicio <= t_ini < horario.horaFin:
                    horario_id_bloque = horario.idHorario
                    if horario.idHorario not in horarios_ids:
                        horarios_ids.append(horario.idHorario)
                    
                    estado_bloque = horario.estado.value if hasattr(horario.estado, 'value') else horario.estado
                    tramo_nombre = "Regular"
                    
                    # IMPORTANTE: Ordenar excepciones por ID descendente
                    excepciones_ordenadas = sorted(
                        horario.excepciones,
                        key=lambda ex: ex.idExcepcion,
                        reverse=True  # La más reciente primero
                    )
                    
                    # Buscar la PRIMERA excepción que aplique (la más reciente)
                    for excepcion in excepciones_ordenadas:
                        if (excepcion.fechaInicio <= fecha_consulta <= excepcion.fechaFin
                            and excepcion.horaInicio <= t_ini < excepcion.horaFin):
                            estado_bloque = excepcion.estado.value if hasattr(excepcion.estado, 'value') else excepcion.estado
                            tramo_nombre = "Excepción"
                            es_exce = True
                            break  # Usar la más reciente
                    
                    # Una vez encontrado el horario para esta hora, salir del bucle
                    break
            
            bloques_del_dia.append({
                "tramo": tramo_nombre,
                "horaInicio": t_ini.strftime("%H:%M"),
                "horaFin": t_fin.strftime("%H:%M"),
                "estado": estado_bloque,
                "esExcepcion": es_exce,
                "horarioId": horario_id_bloque
            })

        resultado_agenda.append({
            "id": horarios_ids[0] if horarios_ids else None,
            "ids": horarios_ids,
            "fecha": fecha_consulta.isoformat(),
            "diaNombre": self._obtener_nombre_dia(fecha_consulta),
            "bloques": bloques_del_dia
        })

     return resultado_agenda

    def _obtener_nombre_dia(self, fecha: date):
        nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        return nombres[fecha.weekday()]