from app.domain.entities import Reserva, ReservaLaboral, ReservaEquipo, equipo, reserva
from ..interfaces.service.IReservaService import IReservaService
from ..interfaces.repository.IReservasRepository import IReservaRepository
from ..interfaces.repository.IHorarioRepository import IHorarioRepository
from ..interfaces.repository.IAreaRepository import IAreaRepository
from ..interfaces.repository.IUsuarioRepository import IUsuarioRepository
from ..interfaces.repository.IEquipoRepository import IEquipoRepository
from ..dtos.reserva import ReservaAlumnoCreateDTO, ObtenerAgendaDTO, ReservaDeleteDTO, ReservaDetailsDTO, EstadoUsoUpdateDTO, ReservaEquipoDTO
from datetime import date, time, timedelta, datetime
from app.domain.entities.reservaEquipo import EstadoUso
from app.persistence.models.enums import  EstadoUsoEquipo, EstadoEquipo

class ReservaService(IReservaService):
    def __init__(self, repository: IReservaRepository, repositoryHorario: IHorarioRepository, repositoryArea: IAreaRepository, repositoryUsuario: IUsuarioRepository, repositoryEquipo: IEquipoRepository):
        self.repository = repository
        self.repositoryHorario = repositoryHorario
        self.repositoryArea = repositoryArea
        self.repositoryUsuario = repositoryUsuario
        self.repositoryEquipo = repositoryEquipo
         

    # Creacion de reserva de Gimnasio, TRX, Cancha Bolada, Cancha de Tenis, Cardio
    def reservaUsuario1(self, dto: ReservaAlumnoCreateDTO):
     horarios = self.repositoryHorario.buscarPorFecha(dto.fechaReserva)

     if not horarios:
        raise ValueError("No hay un horario configurado para esta fecha.")

     horario_seleccionado = None
     for h in horarios:
        if h.idHorario == dto.horarioId:
            horario_seleccionado = h
            break
    
     if not horario_seleccionado:
        raise ValueError(f"El horario con ID {dto.horarioId} no está disponible para esta fecha.")

     excepcion_activa = None
    
    
     excepciones_ordenadas = sorted(
        horario_seleccionado.excepciones,
        key=lambda exc: exc.idExcepcion,
        reverse=True  
    )
    
     for exc in excepciones_ordenadas:
        if exc.fechaInicio <= dto.fechaReserva <= exc.fechaFin:
            if dto.horaInicio < exc.horaFin and dto.horaFin > exc.horaInicio:
                excepcion_activa = exc
                break  

     if excepcion_activa:
        if excepcion_activa.estado.value != "Abierto":
            raise ValueError(f"Horario no disponible debido a una excepción")
     else:
        if horario_seleccionado.estado.value != "Abierto":
            raise ValueError("El horario base está cerrado.")
        
        if dto.horaInicio < horario_seleccionado.horaInicio or dto.horaFin > horario_seleccionado.horaFin:
            raise ValueError(f"La reserva debe estar entre {horario_seleccionado.horaInicio} y {horario_seleccionado.horaFin}")
    
     area = self.repositoryArea.opteberAreaPorId(dto.areaId)
     if not area:
        raise ValueError("El área no existe")
    
    # 5. Verificar usuario
     usuariodb = self.repositoryUsuario.obtenerUsuarioPorId(dto.usuarioId)
     if not usuariodb:
        raise ValueError("Usuario no encontrado")

    # 6. Verificar reservas existentes
     if usuariodb.rol in [2, 3, 4]:
        reservas_existentes = self.repository.listaReservas(
            dto.fechaReserva, dto.horaInicio, dto.horaFin
        )  
        
        # Reglas para áreas 4 y 5 (solo una reserva por bloque)
        if dto.areaId in [4, 5]:
            ocupado = any(
                r for r in reservas_existentes 
                if r.areaId == dto.areaId and r.estado != "Cancelado"
            )
            if ocupado:
                raise ValueError(
                    f"La {area.nombreArea} ya tiene una reserva activa en este horario. "
                    "Solo se permite una reserva por bloque en esta área." 
                )
        
        # Verificar conflictos con otras reservas
        for r_existente in reservas_existentes:
            if r_existente.areaId == dto.areaId:
                if dto.horaInicio < r_existente.horaFin and dto.horaFin > r_existente.horaInicio:
                    rol_existente = r_existente.usuario.rolId
                    
                    # Reglas para profesores
                    if usuariodb.rol == 3:
                        if dto.tipoReserva and dto.tipoReserva.value == "Laboral":
                            raise ValueError(
                                f"No puedes reservar el área {area.nombreArea}. "
                                f"Ya existen reservas en el horario {r_existente.horaInicio} - {r_existente.horaFin}."
                            )
                        
                        if dto.tipoReserva and dto.tipoReserva.value == "Personal":
                            if rol_existente == 3 and r_existente.tipoReserva and r_existente.tipoReserva.value == "Laboral":
                                raise ValueError(
                                    f"No puedes realizar una reserva en el área {area.nombreArea} "
                                    f"porque ya existe una Clase/Reserva programada por un profesor "
                                    f"en el horario {r_existente.horaInicio} - {r_existente.horaFin}."
                                )

                    # Reglas para alumnos y personal
                    if usuariodb.rol in [2, 4]:
                        if rol_existente == 3 and r_existente.tipoReserva and r_existente.tipoReserva.value == "Laboral":
                            raise ValueError(f"No puedes reservar el {area.nombreArea} ya existe una reserva hecha por un profesor")

     if dto.tipoReserva and dto.tipoReserva.value == "Laboral":
        # Reserva laboral (para profesores)
        nuevaReservaLab = ReservaLaboral(
            fechaReserva=dto.fechaReserva,
            horaInicio=dto.horaInicio,
            horaFin=dto.horaFin,
            tipoReserva=dto.tipoReserva,
            area=dto.areaId,
            usuario=usuariodb,
            horario=horario_seleccionado.idHorario,
            claseImpartir=dto.claseImpartir, 
            licenciatura=dto.licId                 
        )
        self.repository.reservaLaboral(nuevaReservaLab)
    
     elif dto.areaId == 2 and usuariodb.rol in [2, 3, 4]:
        # Área de Cardio - requiere equipos
        if not dto.equipoId or len(dto.equipoId) == 0:
            raise ValueError("Para el área de Cardio debes seleccionar al menos una máquina.")
        
        # Verificar disponibilidad de equipos
        for eid in dto.equipoId:
            maquina = self.repositoryEquipo.obtenerEquipoPorId(eid) 
            if maquina.estado != EstadoEquipo.DISPONIBLE:
                raise ValueError(f"La máquina {maquina.nombre} (#{maquina.idEquipo}) no está disponible para reserva.")
        
        # Crear reserva base
        nuevaReserva = Reserva(
            fechaReserva=dto.fechaReserva,
            horaInicio=dto.horaInicio,
            horaFin=dto.horaFin,
            tipoReserva=dto.tipoReserva,
            area=dto.areaId,
            usuario=dto.usuarioId,
            horario=horario_seleccionado.idHorario
        )
        reserva_guardada = self.repository.reservaUsuario1(nuevaReserva)
        
        # Agregar equipos a la reserva
        if dto.equipoId:
            for idequipo in dto.equipoId:
                datosCardio = ReservaEquipo(
                    reserva=reserva_guardada,
                    equipo=idequipo
                )
                self.repository.reservaCardio(datosCardio)
    
     else:
        # Reserva normal
        nuevaReserva = Reserva(
            fechaReserva=dto.fechaReserva,
            horaInicio=dto.horaInicio,
            horaFin=dto.horaFin,
            tipoReserva=dto.tipoReserva,
            area=dto.areaId,
            usuario=dto.usuarioId,
            horario=horario_seleccionado.idHorario
        )
        self.repository.reservaUsuario1(nuevaReserva)
    
     return f"Tu reserva ha sido registrada para el día {dto.fechaReserva} de {dto.horaInicio} a {dto.horaFin} en el área de {area.nombreArea}"
    
    #Muestra el horario para la semana actual y las reservas echas por el usuario que inicio sesion 
    def obtenerAgendaRangoUsuario(self, dto: ObtenerAgendaDTO):
        # 1. Limpieza automática de retrasos
        self.repository.cancelarReservasPorRetraso()

        # 2. Configuración de la semana actual (Lunes a Sábado)
        hoy = date.today()
        lunes_actual = hoy - timedelta(days=hoy.weekday())
        sabado_actual = lunes_actual + timedelta(days=5)

        # 3. Obtener datos de la BD
        horarios_db = self.repository.obtenerAgendaRangoUsuario(lunes_actual, sabado_actual, dto.usuarioId)
        resultado_agenda = []

        HORA_INICIO_FICTICIO = 6
        HORA_FIN_FICTICIO = 19
        dias_nombres_map = {1: "Lunes", 2: "Martes", 3: "Miércoles", 4: "Jueves", 5: "Viernes", 6: "Sábado"}

        for i in range(1, 7):  # Lunes a Sábado
            fecha_consulta = lunes_actual + timedelta(days=i-1)
            dia_semana_id = i
            
            # Filtrar horarios que aplican a este día específico de la semana
            horarios_del_dia = [
                h for h in horarios_db 
                if h.fechaInicio <= fecha_consulta <= h.fechaFin 
                and dia_semana_id in [d.idDia for d in h.dias]
            ]
            
            bloques = []

            for hora in range(HORA_INICIO_FICTICIO, HORA_FIN_FICTICIO):
                t_ini = time(hora, 0)
                t_end = time(hora + 1, 0)
                
                estado_bloque = "Sin horario asignado"
                tipo_bloque = "Sin horario"
                horario_id_bloque = None
                
                # --- Lógica de Horario y Excepciones ---
                for horario in horarios_del_dia:
                    if horario.horaInicio <= t_ini < horario.horaFin:
                        horario_id_bloque = horario.idHorario
                        estado_bloque = getattr(horario.estado, 'value', horario.estado)
                        tipo_bloque = "Regular"
                        
                        # BUSCAR LA ÚLTIMA EXCEPCIÓN (ID más alto primero)
                        excepciones_validas = [
                            ex for ex in horario.excepciones
                            if ex.fechaInicio <= fecha_consulta <= ex.fechaFin
                            and ex.horaInicio <= t_ini < ex.horaFin
                        ]
                        
                        if excepciones_validas:
                            # Ordenamos por ID descendente para tomar la creación más reciente
                            ultima_excep = sorted(excepciones_validas, key=lambda x: x.idExcepcion, reverse=True)[0]
                            estado_bloque = getattr(ultima_excep.estado, 'value', ultima_excep.estado)
                            tipo_bloque = "Excepción"
                        
                        break # Salir del bucle de horarios tras encontrar el correspondiente

                # --- Lógica de Reservas del Usuario ---
                mi_reserva = None
                for h_busqueda in horarios_db:
                    res = next((r for r in h_busqueda.reservas 
                                if r.usuarioId == dto.usuarioId 
                                and r.fechaReserva == fecha_consulta
                                and r.horaInicio <= t_ini < r.horaFin), None)
                    if res:
                        mi_reserva = res
                        break

                # Datos de área y licenciatura
                nombre_area = None
                clase = None
                nombreLic = "N/A"

                if mi_reserva:
                    area_obj = self.repositoryArea.opteberAreaPorId(mi_reserva.areaId)
                    nombre_area = area_obj.nombreArea if area_obj else None
                    
                    res_lab = getattr(mi_reserva, 'reserva_laboral', None)
                    if res_lab:
                        clase = res_lab.claseImpartir
                        lic_obj = getattr(res_lab, 'licenciatura', None)
                        nombreLic = lic_obj.nombreLic if lic_obj else "N/A"

                bloques.append({
                    "horaInicio": t_ini.strftime("%H:%M"),
                    "horaFin": t_end.strftime("%H:%M"),
                    "estado": estado_bloque,
                    "tipo": tipo_bloque,
                    "tipoReserva": getattr(mi_reserva.tipoReserva, 'value', mi_reserva.tipoReserva) if mi_reserva else None,
                    "claseImpartir": clase,
                    "licenciatura": nombreLic,
                    "reservadoPorMi": mi_reserva is not None,
                    "idReserva": mi_reserva.idReserva if mi_reserva else None,
                    "nombreArea": nombre_area,
                    "estado_reserva": getattr(mi_reserva.estado, 'value', mi_reserva.estado) if mi_reserva else None,
                    "horarioId": horario_id_bloque
                })

            resultado_agenda.append({
                "fecha": fecha_consulta.isoformat(),
                "diaNombre": dias_nombres_map[i], 
                "bloques": bloques,
                "ids": list(set([h.idHorario for h in horarios_del_dia]))
            })

        return resultado_agenda

    def _obtener_nombre_dia(self, fecha: date) -> str:
        nombres = [
        "Lunes", 
        "Martes", 
        "Miércoles", 
        "Jueves", 
        "Viernes", 
        "Sábado", 
        "Domingo"
          ]
        return nombres[fecha.weekday()]
    
    # Cancelación de reservas
    def cancelarReserva(self, dto: ReservaDeleteDTO):
       dbReserva = self.repository.cancelarReserva(dto.idReserva, dto.usuarioId)

       if not dbReserva:
          raise ValueError("Ocurrio un error al cancelar la reserva")
       
       return  "Reserva cacelada con exito"
    
    # Detalle de la reserva en el area de cardio
    def detalleReserva(self, dto: ReservaDetailsDTO):
     reserva = self.repository.detalleReserva(dto.idReserva)
     if not reserva:
        return {"error": "Reserva no encontrada"}

     ahora = datetime.now()
     hoy = ahora.date()
     hora_actual = ahora.time()
    
    # Verificar si la reserva ya pasó su horario
     reserva_terminada = reserva.fechaReserva < hoy or (reserva.fechaReserva == hoy and reserva.horaFin <= hora_actual)

     detalle = {
        "id_reserva": reserva.idReserva,
        "nombre_area": reserva.area.nombreArea if reserva.area else None,
        "fechaReserva": reserva.fechaReserva,
        "Asistencia": reserva.estado,
        "hora_inicio": reserva.horaInicio.strftime("%H:%M") if reserva.horaInicio else None,
        "hora_fin": reserva.horaFin.strftime("%H:%M") if reserva.horaFin else None,
        "reserva_terminada": reserva_terminada,
        "maquinas": []
    }

     for re in reserva.reserva_equipos:
        estado_fisico_maquina = re.equipo.estado 
        
        # Obtener horas de inicio y fin del uso de la máquina
        hora_inicio_uso = re.horaInicio.strftime("%H:%M") if hasattr(re, 'horaInicio') and re.horaInicio else None
        hora_fin_uso = re.horaFin.strftime("%H:%M") if hasattr(re, 'horaFin') and re.horaFin else None
        
        # Calcular ocupación global
        ocupacion_global = "Libre"
        
        # Si la reserva ya terminó, siempre está libre
        if reserva_terminada:
            ocupacion_global = "Libre"
        else:
            # Verificar si alguien más está usando el equipo
            ocupada_por_otros = self.repository.estaEquipoEnUsoPorOtros(re.equipoId, reserva)
            ocupacion_global = "En uso" if ocupada_por_otros or re.estadoUso == EstadoUsoEquipo.EN_USO else "Libre"

        id_final = re.equipoId
        mensaje = "Máquina disponible."
        
        # Lógica de Reasignación Automática
        necesita_cambio = (ocupacion_global == "En uso" or estado_fisico_maquina.value != "Disponible")
        
        if necesita_cambio and re.estadoUso == EstadoUsoEquipo.PENDIENTE and not reserva_terminada:
            sustituta = self.repository.buscarMaquinaSustituta(
                re.equipo.nombre, 
                reserva.areaId, 
                re.equipoId
            )
            
            if sustituta:
                self.repository.actualizarEquipoReserva(re.idReservaEquipo, sustituta.idEquipo)
                id_final = sustituta.idEquipo
                razon = "fuera de servicio" if estado_fisico_maquina.value != "Disponible" else "ocupada"
                mensaje = f"REASIGNADA: La original estaba {razon}. Se asignó la #{id_final}."
            else:
                mensaje = "MÁQUINA NO DISPONIBLE: No hay otras máquinas de este tipo libres."
        elif reserva_terminada:
            mensaje = "Reserva finalizada. La máquina está disponible para otros usuarios."

        detalle["maquinas"].append({
            "reserva_Equipo": re.idReservaEquipo,
            "id_asignado": id_final,
            "nombre_maquina": re.equipo.nombre,
            "estado_Uso": re.estadoUso.value if hasattr(re.estadoUso, 'value') else str(re.estadoUso),
            "estado_fisico_maquina": estado_fisico_maquina.value if hasattr(estado_fisico_maquina, 'value') else str(estado_fisico_maquina),
            "ocupacion_global": ocupacion_global,
            "mensaje": mensaje,
            "hora_inicio_uso": hora_inicio_uso,  # Nueva campo
            "hora_fin_uso": hora_fin_uso         # Nueva campo
        })

     return detalle
    
    def cambiarEstadoEquipo(self, dto: EstadoUsoUpdateDTO):
       resultado = self.repository.registrarUsoEquipo(dto.idReservaEquipo)
        
       if not resultado:
            return {"error": "No se encontró el registro"}

       return {
            "mensaje": "Estado actualizado",
            "nuevo_estado": resultado.estadoUso.value,
            "hora": datetime.now().strftime("%H:%M")
        }
    
    def buscarHorario(self, fecha: date, dto: ObtenerAgendaDTO):
     self.repository.cancelarReservasPorRetraso()
     lunes_actual = fecha - timedelta(days=fecha.weekday())
     sabado_actual = lunes_actual + timedelta(days=5) 

     horarios_db = self.repository.obtenerAgendaRangoUsuario(lunes_actual, sabado_actual, dto.usuarioId)
     resultado_agenda = []

    # Rango operativo solicitado (6 AM a 7 PM)
     HORA_INICIO_FICTICIO = 6
     HORA_FIN_FICTICIO = 19

     for i in range(6):  # Iterar de Lunes a Sábado
        fecha_consulta = lunes_actual + timedelta(days=i)
        dia_semana_id = i + 1 
        
        # 1. Filtramos los horarios que aplican para este día de la semana
        # Nota: Usamos una lista en lugar de next() por si hay horarios solapados
        horarios_del_dia = [h for h in horarios_db if any(d.idDia == dia_semana_id for d in h.dias)]
        
        bloques = []

        for hora in range(HORA_INICIO_FICTICIO, HORA_FIN_FICTICIO):
            t_ini = time(hora, 0)
            t_end = time(hora + 1, 0)
            
            estado_bloque = "SIN PROGRAMACIÓN"
            tipo_bloque = "VACÍO"
            horario_id_bloque = None
            # 2. Lógica de Horario Regular y Excepciones
            for h_busqueda in horarios_del_dia:
                if h_busqueda.horaInicio <= t_ini < h_busqueda.horaFin:
                    estado_bloque = getattr(h_busqueda.estado, 'value', h_busqueda.estado)
                    tipo_bloque = "REGULAR"
                    horario_id_bloque = h_busqueda.idHorario
                    
                    # --- CORRECCIÓN: Filtrar y ordenar excepciones por ID descendente ---
                    excepciones_validas = [
                        ex for ex in h_busqueda.excepciones 
                        if ex.fechaInicio <= fecha_consulta <= ex.fechaFin
                        and ex.horaInicio <= t_ini < ex.horaFin
                    ]
                    
                    if excepciones_validas:
                        # Tomamos la excepción con el ID más alto (la última creada)
                        ultima_excep = sorted(excepciones_validas, key=lambda x: x.idExcepcion, reverse=True)[0]
                        estado_bloque = getattr(ultima_excep.estado, 'value', ultima_excep.estado)
                        tipo_bloque = "EXCEPCIÓN"
                    
                    break # Encontramos el horario base para esta hora, pasamos a las reservas

            # 3. Lógica de Reservas (Misma lógica de búsqueda)
            mi_reserva = None
            for h_item in horarios_db:
                res = next((r for r in h_item.reservas 
                            if r.usuarioId == dto.usuarioId 
                            and r.fechaReserva == fecha_consulta
                            and r.horaInicio <= t_ini < r.horaFin), None)
                if res:
                    mi_reserva = res
                    break

            # Datos adicionales (Área, Clase, Licenciatura)
            nombre_area = None
            clase = None
            nombreLic = "N/A"
           

            if mi_reserva:
                area_obj = self.repositoryArea.opteberAreaPorId(mi_reserva.areaId)
                nombre_area = area_obj.nombreArea if area_obj else None
                
                res_lab = getattr(mi_reserva, 'reserva_laboral', None)
                if res_lab:
                    clase = res_lab.claseImpartir
                    lic_obj = getattr(res_lab, 'licenciatura', None)
                    nombreLic = lic_obj.nombreLic if lic_obj else "N/A"
                    

            bloques.append({
                "horaInicio": t_ini.strftime("%H:%M"),
                "horaFin": t_end.strftime("%H:%M"),
                "estado": estado_bloque,
                "tipo": tipo_bloque,
                "tipoReserva": getattr(mi_reserva.tipoReserva, 'value', mi_reserva.tipoReserva) if mi_reserva else None,
                "claseImpartir": clase,
                "licenciatura": nombreLic,
                "reservadoPorMi": mi_reserva is not None,
                "idReserva": mi_reserva.idReserva if mi_reserva else None,
                "nombreArea": nombre_area,
                "estado_reserva": getattr(mi_reserva.estado, 'value', mi_reserva.estado) if mi_reserva else None,
                "horarioId" : horario_id_bloque
            })

        resultado_agenda.append({
            "fecha": fecha_consulta.isoformat(),
            "diaNombre": self._obtener_nombre_dia(fecha_consulta),
            "bloques": bloques
        })

     return resultado_agenda
    
    ##################
    def agregarEquipoAdicional(self, dto: ReservaEquipoDTO):
      reserva = self.repository.obtenerReservaPorId(dto.id_reserva)
      hoy = datetime.now().date()
    
      if not reserva or reserva.fechaReserva != hoy:
        raise ValueError("Solo puedes agregar máquinas a una reserva del día de hoy.")

      equipo = self.repositoryEquipo.obtenerEquipoPorId(dto.id_equipo)
      if equipo.estado != EstadoEquipo.DISPONIBLE:
        raise ValueError(f"La máquina {equipo.nombre} no está disponible actualmente.")

      if self.repository.estaEquipoEnUsoPorOtros(dto.id_equipo, reserva):
        raise ValueError("Esta máquina está siendo usada por alguien más.")

      return self.repository.agregarEquipoAReserva(dto.id_reserva, dto.id_equipo)