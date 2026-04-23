from app.domain.entities import Horario, Reserva
from app.application.interfaces.repository.IAsistenciasyReservasRepository import IAsistenciasyReservasRepository
from app.application.interfaces.repository.IReservasRepository import IReservaRepository
from app.application.interfaces.service.IAsistenciasyReservasService import IAsistenciasyReservasService
from datetime import datetime, time, timedelta, date
from app.domain.entities.reserva import Estado
from app.domain.entities import Usuario, Alumno
from app.application.dtos.reserva import AsistenciaResponseDTO


class AsistenciasyReservasService(IAsistenciasyReservasService):

    def __init__(self, repository: IAsistenciasyReservasRepository, repositoryReserva: IReservaRepository):
        self.repository = repository
        self.repositoryReserva = repositoryReserva


    def obtenerHorariosAsistenciasyReservas(self, idArea: int):
    # Obtener todos los horarios sin filtro de área
     horarios_db = self.repository.obtenerHorariosAsistenciasyReservas(idArea)
     self.repositoryReserva.cancelarReservasPorRetraso()
    
     hoy = date.today()
     lunes_actual = hoy - timedelta(days=hoy.weekday())
    
     HORA_INICIO_FICTICIO = 6
     HORA_FIN_FICTICIO = 19
    
     resultado_semanal = []
    
     print(f"=== Procesando área ID: {idArea} ===")
     print(f"Total horarios encontrados: {len(horarios_db)}")
    
     for i in range(1, 7):  # Lunes a Sábado (1=Lunes, 6=Sábado)
        fecha_evaluar = lunes_actual + timedelta(days=i-1)
        dia_nombre = self._obtener_nombre_dia(fecha_evaluar)
        
        bloques_del_dia = []
        
        for hora in range(HORA_INICIO_FICTICIO, HORA_FIN_FICTICIO):
            t_ini = time(hora, 0)
            t_end = time(hora + 1, 0)
            
            estado_horario = "Sin programación"
            es_exce = False
            excepcion_id = None
            excepcion_fecha_creacion = None
            excepcion_motivo = None
            horario_id = None
            
            # --- Buscar si existe un horario configurado para esta hora y día ---
            horario_encontrado = None
            for h in horarios_db:
                if not h.dias:
                    continue
                if not (h.fechaInicio <= fecha_evaluar <= h.fechaFin):
                    continue
                if not any(d.idDia == i for d in h.dias):
                    continue
                if not (h.horaInicio <= t_ini < h.horaFin):
                    continue
                horario_encontrado = h
                break
            
            # --- Obtener reservas del bloque ---
            usuarios_list = []
            conteo_ocupacion = 0
            
            if horario_encontrado:
                horario_id = horario_encontrado.idHorario
                estado_horario = getattr(horario_encontrado.estado, 'value', horario_encontrado.estado)
                
                # Revisar si hay excepciones activas para este bloque
                excepciones_validas = [
                    ex for ex in horario_encontrado.excepciones 
                    if ex.fechaInicio <= fecha_evaluar <= ex.fechaFin
                    and ex.horaInicio <= t_ini < ex.horaFin
                ]
                
                if excepciones_validas:
                    ultima_excepcion = sorted(excepciones_validas, key=lambda x: x.idExcepcion, reverse=True)[0]
                    estado_horario = getattr(ultima_excepcion.estado, 'value', ultima_excepcion.estado)
                    es_exce = True
                    excepcion_id = ultima_excepcion.idExcepcion
                    excepcion_fecha_creacion = ultima_excepcion.created_at if hasattr(ultima_excepcion, 'created_at') else None
                    excepcion_motivo = ultima_excepcion.motivo if hasattr(ultima_excepcion, 'motivo') else None
                
                # Procesar TODAS las reservas del bloque (incluyendo canceladas)
                if horario_encontrado.reservas:
                    for r in horario_encontrado.reservas:
                        # Verificar que la reserva coincida con este bloque Y sea del área correcta
                        if (r.horaInicio == t_ini and 
                            r.fechaReserva == fecha_evaluar and 
                            r.areaId == idArea):
                            
                            estado_reserva = getattr(r.estado, 'value', str(r.estado))
                            estado_reserva_lower = estado_reserva.lower()
                            
                            # Obtener motivo de cancelación si existe
                            motivo = getattr(r.motivoCancelacion, 'value', r.motivoCancelacion) if r.motivoCancelacion else None
                            
                            # Obtener rol del usuario
                            nombre_rol = "Sin Rol"
                            if r.usuario and hasattr(r.usuario, 'rol') and r.usuario.rol:
                                nombre_rol = r.usuario.rol.nombreRol
                            
                            # CONTAR para ocupación SOLO si NO está cancelada y está activa
                            if estado_reserva_lower != "cancelado":
                                if estado_reserva_lower in ["pendiente", "asistió", "asistio"]:
                                    conteo_ocupacion += 1
                            
                            # AGREGAR a la lista TODAS las reservas (incluyendo canceladas)
                            usuarios_list.append({
                                "reservaId": r.idReserva,
                                "id": r.usuario.idUsuario if r.usuario else None,
                                "foto": r.usuario.foto if r.usuario else None,
                                "usuario": f"{r.usuario.nombre} {getattr(r.usuario, 'apellido', '')}".strip() if r.usuario else "Usuario no disponible",
                                "rol": nombre_rol,
                                "estado Reserva": estado_reserva,
                                "motivoCancelacion": motivo
                            })
            
            # --- Construcción del bloque con IDs ---
            bloque_data = {
                "horaInicio": t_ini.strftime("%H:%M"),
                "horaFin": t_end.strftime("%H:%M"),
                "rango": f"{t_ini.strftime('%H:%M')} - {t_end.strftime('%H:%M')}",
                "estadoHorario": estado_horario,
                "esExcepcion": es_exce,
                "ocupacion": f"{conteo_ocupacion}/10",
                "disponibles": max(0, 10 - conteo_ocupacion),
                "usuarios": usuarios_list
            }
            
            # Asignar IDs según corresponda
            if es_exce:
                bloque_data["id"] = f"exc_{excepcion_id}_{hora}" if excepcion_id else None
                bloque_data["horarioId"] = horario_id
                bloque_data["excepcionId"] = excepcion_id
                bloque_data["excepcion"] = {
                    "id": excepcion_id,
                    "fecha_creacion": excepcion_fecha_creacion,
                    "motivo": excepcion_motivo
                }
            elif horario_id:
                bloque_data["id"] = f"{horario_id}_{hora}"
                bloque_data["horarioId"] = horario_id
            else:
                bloque_data["id"] = None
                bloque_data["horarioId"] = None
            
            bloques_del_dia.append(bloque_data)
        
        resultado_semanal.append({
            "dia": dia_nombre,
            "fecha": fecha_evaluar.strftime("%Y-%m-%d"),
            "bloques": bloques_del_dia
        })
    
     return resultado_semanal


    def obtenerHorariosAsistenciasyReservasPorFecha(self, fecha_referencia: date, idArea: int):

    # Obtener todos los horarios sin filtro de área
     horarios_db = self.repository.obtenerHorariosAsistenciasyReservas(idArea)
     self.repositoryReserva.cancelarReservasPorRetraso()
    

     dias_a_lunes = fecha_referencia.weekday()
     lunes_semana = fecha_referencia - timedelta(days=dias_a_lunes)
    
     HORA_INICIO_FICTICIO = 6
     HORA_FIN_FICTICIO = 19
    
     resultado_semanal = []
    
 
    
     for i in range(1, 7):  # Lunes a Sábado (1=Lunes, 6=Sábado)
        fecha_evaluar = lunes_semana + timedelta(days=i-1)
        dia_nombre = self._obtener_nombre_dia(fecha_evaluar)
        
        bloques_del_dia = []
        
        for hora in range(HORA_INICIO_FICTICIO, HORA_FIN_FICTICIO):
            t_ini = time(hora, 0)
            t_end = time(hora + 1, 0)
            
            estado_horario = "Sin programación"
            es_exce = False
            excepcion_id = None
            excepcion_fecha_creacion = None
            excepcion_motivo = None
            horario_id = None
            
            # --- Buscar si existe un horario configurado para esta hora y día ---
            horario_encontrado = None
            for h in horarios_db:
                if not h.dias:
                    continue
                if not (h.fechaInicio <= fecha_evaluar <= h.fechaFin):
                    continue
                if not any(d.idDia == i for d in h.dias):
                    continue
                if not (h.horaInicio <= t_ini < h.horaFin):
                    continue
                horario_encontrado = h
                break
            
            # --- Obtener reservas del bloque ---
            usuarios_list = []
            conteo_ocupacion = 0
            
            if horario_encontrado:
                horario_id = horario_encontrado.idHorario
                estado_horario = getattr(horario_encontrado.estado, 'value', horario_encontrado.estado)
                
                # Revisar si hay excepciones activas para este bloque
                excepciones_validas = [
                    ex for ex in horario_encontrado.excepciones 
                    if ex.fechaInicio <= fecha_evaluar <= ex.fechaFin
                    and ex.horaInicio <= t_ini < ex.horaFin
                ]
                
                if excepciones_validas:
                    ultima_excepcion = sorted(excepciones_validas, key=lambda x: x.idExcepcion, reverse=True)[0]
                    estado_horario = getattr(ultima_excepcion.estado, 'value', ultima_excepcion.estado)
                    es_exce = True
                    excepcion_id = ultima_excepcion.idExcepcion
                    excepcion_fecha_creacion = ultima_excepcion.created_at if hasattr(ultima_excepcion, 'created_at') else None
                    excepcion_motivo = ultima_excepcion.motivo if hasattr(ultima_excepcion, 'motivo') else None
                
                # Procesar TODAS las reservas del bloque (incluyendo canceladas)
                if horario_encontrado.reservas:
                    for r in horario_encontrado.reservas:
                        # Verificar que la reserva coincida con este bloque Y sea del área correcta
                        if (r.horaInicio == t_ini and 
                            r.fechaReserva == fecha_evaluar and 
                            r.areaId == idArea):
                            
                            estado_reserva = getattr(r.estado, 'value', str(r.estado))
                            estado_reserva_lower = estado_reserva.lower()
                            
                            # Obtener motivo de cancelación si existe
                            motivo = getattr(r.motivoCancelacion, 'value', r.motivoCancelacion) if r.motivoCancelacion else None
                            
                            # Obtener rol del usuario
                            nombre_rol = "Sin Rol"
                            if r.usuario and hasattr(r.usuario, 'rol') and r.usuario.rol:
                                nombre_rol = r.usuario.rol.nombreRol
                            
                            # CONTAR para ocupación SOLO si NO está cancelada y está activa
                            if estado_reserva_lower != "cancelado":
                                if estado_reserva_lower in ["pendiente", "asistió", "asistio"]:
                                    conteo_ocupacion += 1
                            
                            # AGREGAR a la lista TODAS las reservas (incluyendo canceladas)
                            usuarios_list.append({
                                "reservaId": r.idReserva,
                                "id": r.usuario.idUsuario if r.usuario else None,
                                "foto": r.usuario.foto if r.usuario else None,
                                "usuario": f"{r.usuario.nombre} {getattr(r.usuario, 'apellido', '')}".strip() if r.usuario else "Usuario no disponible",
                                "rol": nombre_rol,
                                "estado Reserva": estado_reserva,
                                "motivoCancelacion": motivo
                            })
            
            # --- Construcción del bloque con IDs  ---
            bloque_data = {
                "horaInicio": t_ini.strftime("%H:%M"),
                "horaFin": t_end.strftime("%H:%M"),
                "rango": f"{t_ini.strftime('%H:%M')} - {t_end.strftime('%H:%M')}",
                "estadoHorario": estado_horario,
                "esExcepcion": es_exce,
                "ocupacion": f"{conteo_ocupacion}/10",
                "disponibles": max(0, 10 - conteo_ocupacion),
                "usuarios": usuarios_list
            }
            
            # Asignar IDs según corresponda
            if es_exce:
                bloque_data["id"] = f"exc_{excepcion_id}_{hora}" if excepcion_id else None
                bloque_data["horarioId"] = horario_id
                bloque_data["excepcionId"] = excepcion_id
                bloque_data["excepcion"] = {
                    "id": excepcion_id,
                    "fecha_creacion": excepcion_fecha_creacion,
                    "motivo": excepcion_motivo
                }
            elif horario_id:
                bloque_data["id"] = f"{horario_id}_{hora}"
                bloque_data["horarioId"] = horario_id
            else:
                bloque_data["id"] = None
                bloque_data["horarioId"] = None
            
            bloques_del_dia.append(bloque_data)
        
        resultado_semanal.append({
            "dia": dia_nombre,
            "fecha": fecha_evaluar.strftime("%Y-%m-%d"),
            "bloques": bloques_del_dia
        })
    
     return resultado_semanal


    def _obtener_nombre_dia(self, fecha: date):
     nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
     return nombres[fecha.weekday()]
    
    def detallesUsuarioReserva(self, idReserva: int) -> dict:
     reserva = self.repository.detallesUsuarioReserva(idReserva)
     if not reserva:
        return None

     usuario = reserva.usuario
    
    # Campos base que tienen TODOS los usuarios
     detalles = {
        "reservaId": reserva.idReserva,
        "estado_reserva": getattr(reserva.estado, 'value', reserva.estado),
        "rol_usuario": usuario.rol.nombreRol if usuario.rol else "N/A",
        "foto": usuario.foto,
        "nombre": usuario.nombre,
        "correo": usuario.correo
     }

     # Campos EXCLUSIVOS de Alumno
     if isinstance(usuario, Alumno):
        detalles["nivel_academico"] = usuario.nivel.nombreNivel if usuario.nivel else "N/A"
        detalles["licenciatura"] = usuario.licenciatura.nombreLic if usuario.licenciatura else "N/A"

     # Información de Cardio
     if int(reserva.areaId) == 2:
        maquinas_info = []
        equipos = getattr(reserva, 'reserva_equipos', [])
        
        if equipos:
            for re in equipos:
                nombre = "Equipo no identificado"
                if re.equipo:
                    nombre = re.equipo.nombre 
                
                maquinas_info.append({
                    "nombre_equipo": nombre,
                    "hora_inicio": re.horaInicio.strftime("%H:%M") if re.horaInicio else "N/A",
                    "hora_fin": re.horaFin.strftime("%H:%M") if re.horaFin else "N/A"
                })
        detalles["info_cardio"] = maquinas_info

    # Detalle Laboral (Profesores)
     laboral = reserva.reserva_laboral
     es_docente = usuario.rol and (usuario.rol.nombreRol in ["Docente", "Profesor"])
     if es_docente or getattr(reserva, 'es_laboral', False):
        tipo = getattr(reserva.tipo_reserva, 'value', reserva.tipo_reserva)
        detalles["detalle_laboral"] = {
            "tipo_reserva": tipo,
            "clase":laboral.claseImpartir if laboral else "N/A",
            "licenciatura_destino": laboral.licenciatura.nombreLic if (laboral and laboral.licenciatura) else "N/A"
        }

     return detalles
    

    def registrarAsistencia(self, idReserva: int) -> AsistenciaResponseDTO:
     reserva_db = self.repository.obtenerReservaPorId(idReserva) 
    
     if not reserva_db:
        raise ValueError("Reserva no encontrada")

     ahora = datetime.now()
     hoy = ahora.date()

     if reserva_db.fechaReserva != hoy:
        raise ValueError(f"La reserva es para el día {reserva_db.fechaReserva}. Hoy es {hoy}.")

  
     dt_inicio = datetime.combine(reserva_db.fechaReserva, reserva_db.horaInicio)
     dt_fin = datetime.combine(reserva_db.fechaReserva, reserva_db.horaFin)
    
     margen_apertura = dt_inicio 

    
     if ahora < margen_apertura:
        raise ValueError(f"Aún no puedes marcar asistencia. Se habilita a las {margen_apertura.strftime('%H:%M')}")

     if ahora > dt_fin:
        raise ValueError(f"La reserva ha expirado. Terminó a las {dt_fin.strftime('%H:%M')}")

    
     self.repository.registrarAsistencia(idReserva)
    
     return AsistenciaResponseDTO(
        idReserva=idReserva,
        mensaje="Asistencia confirmada correctamente",
        nuevo_estado="Asistió",
        exito=True
    )