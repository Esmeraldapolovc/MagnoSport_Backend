from app.application.interfaces.repository.IReservasRepository import IReservaRepository
from app.persistence.models import Reserva as ReservaModel
from app.persistence.models import Horario as HorarioModel, Usuario
from app.persistence.models import ReservaLaboral as ReservaLaboralModel
from app.persistence.models import ReservaEquipo as ReservaEquipoModel, Equipo
from app.domain.entities import Reserva, ReservaLaboral, ReservaEquipo
from sqlalchemy.orm import Session, joinedload, relationship, contains_eager
from app.persistence.models.enums import EstadoReserva
from typing  import List
from datetime import date, time, datetime, timedelta
from app.persistence.models.enums import tipoReserva, EstadoUsoEquipo, MotivoCancelacion, EstadoEquipo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func
from fastapi import HTTPException

class ReservaRepository(IReservaRepository):

    def __init__(self, db: Session):
        self.db = db


    # Reserva de Gimnasio, TRX, Cancha Bolada, Cancha de Tenis, cardio
    def reservaUsuario1(self, reserva: Reserva) ->Reserva:
        try:
            # Filtramos por: Misma Área + Misma Fecha + Mismo Rango de Horas
            
            total_reservas = (
                self.db.query(func.count(ReservaModel.idReserva))
                .filter(
                    ReservaModel.areaId == reserva.area,
                    func.date(ReservaModel.fechaReserva) == reserva.fechaReserva,
                    ReservaModel.horaInicio == reserva.horaInicio,
                    ReservaModel.horaFin == reserva.horaFin,
                    ReservaModel.estado != EstadoReserva.CANCELADO 
                )
                .with_for_update()
                .scalar()
            )

            
            if total_reservas >= 10:
                # Si ya hay 10 o más, lanzamos el error antes de hacer el insert
                raise HTTPException(
                    status_code=400,
                    detail=f"Cupo agotado para el bloque {reserva.horaInicio}-{reserva.horaFin}. (Actual: {total_reservas}/10)"
                )

            dbReserva = ReservaModel(
                fechaReserva=reserva.fechaReserva,
                horaInicio=reserva.horaInicio,
                horaFin=reserva.horaFin,
                estado=EstadoReserva.PENDIENTE,
                tipoReserva=reserva.tipoReserva,
                areaId=reserva.area,
                usuarioId=reserva.usuario,
                horarioId=reserva.horario
            )

            self.db.add(dbReserva)
            self.db.commit()
            self.db.refresh(dbReserva)

            return dbReserva

        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"Error inesperado: {str(e)}")
            raise
    
    def reservaLaboral(self, reservalab: ReservaLaboral) -> ReservaLaboral:
      dbReserva = ReservaModel(
        fechaReserva = reservalab.fechaReserva,
        horaInicio   = reservalab.horaInicio,
        horaFin      = reservalab.horaFin,
        estado       = EstadoReserva.PENDIENTE,
        tipoReserva  = reservalab.tipoReserva,
        areaId       = reservalab.area,
        usuarioId    = reservalab.usuario.idUsuario,
        horarioId    = reservalab.horario
     )

      self.db.add(dbReserva)
      self.db.flush() 
 
      dbReservaLab = ReservaLaboralModel(
        idReserva     = dbReserva.idReserva, 
        claseImpartir = reservalab.claseImpartir,
        licId         = reservalab.licenciatura
    )

      self.db.add(dbReservaLab)
      
      self.db.commit()
    
      reservalab.idReserva = dbReserva.idReserva
    
      return reservalab
   
    
    def reservaCardio(self, reservaCardio: ReservaEquipo) -> ReservaEquipo:
       dbReservaEquipo = ReservaEquipoModel(
          estadoUso = EstadoUsoEquipo.PENDIENTE,
          reservaId = reservaCardio.reserva.idReserva,
          equipoId = reservaCardio.equipo
       )


       self.db.add(dbReservaEquipo)
       self.db.commit()
       self.db.refresh(dbReservaEquipo)

       reservaCardio.idReservaEquipo = dbReservaEquipo.equipoId
       return reservaCardio
    

    # muestra un istado de horarios y reservas  que pertenecen al usuario que inicio sesion 
    def obtenerAgendaRangoUsuario(self, fecha_inicio: date, fecha_fin: date, usuario_id: int):
        return (
            self.db.query(HorarioModel)
            .outerjoin(
                ReservaModel,
                (ReservaModel.horarioId == HorarioModel.idHorario) &
                (ReservaModel.estado != EstadoReserva.CANCELADO) &
                (ReservaModel.usuarioId == usuario_id)
            )
            .options(
                joinedload(HorarioModel.excepciones),
                contains_eager(HorarioModel.reservas)
                .joinedload(ReservaModel.reserva_laboral)
                .joinedload(ReservaLaboralModel.licenciatura)
            )
            .filter(
                HorarioModel.fechaInicio <= fecha_fin,
                HorarioModel.fechaFin >= fecha_inicio
            )
            .all()
        )
    

     # muestra un listado con las reservas echas en una fecha y horas especificas 
    def listaReservas(self, fecha: date, hora_inicio: time, hora_fin: time):
       return self.db.query(ReservaModel)\
        .join(Usuario, ReservaModel.usuarioId == Usuario.idUsuario)\
        .filter(
            ReservaModel.fechaReserva == fecha,
            ReservaModel.horaInicio < hora_fin,
            ReservaModel.horaFin > hora_inicio,
            Usuario.rolId.in_([2, 3, 4]),
            ReservaModel.estado != EstadoReserva.CANCELADO
        ).all()
                    
    
    #Cancelación de reserva
    def cancelarReserva(self, idReserva:int,  usuarioId: int) -> bool:
       dbReserva = self.db.query(ReservaModel).filter(ReservaModel.idReserva == idReserva, ReservaModel.usuarioId == usuarioId).first()

       if not dbReserva:
          return None
       
       dbReserva.estado = EstadoReserva.CANCELADO
       dbReserva.motivoCancelacion = MotivoCancelacion.CANCELACION_POR_USUARIO

       self.db.add(dbReserva)
       self.db.commit()
       self.db.refresh(dbReserva)

       return True

        
    # Obtiene detalle de la reserva en el area de cardio
    def detalleReserva(self, idReserva: int):
     ahora = datetime.now()
     hoy = ahora.date()
     hora_actual = ahora.time()
    
     return self.db.query(ReservaModel)\
        .outerjoin(ReservaModel.area)\
        .outerjoin(ReservaEquipoModel)\
        .outerjoin(Equipo)\
        .options(
            joinedload(ReservaModel.area),         
            joinedload(ReservaModel.usuario),      
            joinedload(ReservaModel.reserva_equipos).joinedload(ReservaEquipoModel.equipo)
        )\
        .filter(ReservaModel.idReserva == idReserva)\
        .first()
   
    def buscarMaquinaSustituta(self, nombre_maquina: str, area_id: int, equipo_actual_id: int):
     hoy = datetime.now().date()
     hora_actual = datetime.now().time()

    # IDs de equipos que están en uso REAL (EN_USO) y aún dentro de su horario
     ids_en_uso_real = self.db.query(ReservaEquipoModel.equipoId).join(ReservaModel).filter(
        ReservaEquipoModel.estadoUso == EstadoUsoEquipo.EN_USO,
        ReservaModel.fechaReserva == hoy,
        ReservaModel.horaFin > hora_actual  # Solo los que aún no han terminado
    ).subquery()

    # Buscamos un equipo que:
    # - Mismo nombre y área
    # - NO esté en uso REAL (EN_USO)
    # - Esté disponible físicamente
     return self.db.query(Equipo).filter(
        Equipo.nombre == nombre_maquina,
        Equipo.areaId == area_id,
        Equipo.idEquipo != equipo_actual_id,
        Equipo.estado == EstadoEquipo.DISPONIBLE,
        ~Equipo.idEquipo.in_(ids_en_uso_real) ).first()

    def estaEquipoEnUsoPorOtros(self, equipo_id: int, reserva_actual: ReservaModel) -> bool:
     ahora = datetime.now()
     hoy = ahora.date()
     hora_actual = ahora.time()
    
    # Buscar si el equipo está en uso REAL (EN_USO) por otra reserva
     existe_otro = self.db.query(ReservaEquipoModel).join(ReservaModel).filter(
        ReservaEquipoModel.equipoId == equipo_id,
        ReservaEquipoModel.reservaId != reserva_actual.idReserva,
        ReservaEquipoModel.estadoUso == EstadoUsoEquipo.EN_USO,
        ReservaModel.fechaReserva == hoy,
        # Solo considerar si la reserva aún no ha terminado su horario
        ReservaModel.horaFin > hora_actual ).first()
    
     return existe_otro is not None
    
 
    def registrarUsoEquipo(self, idReservaEquipo: int) -> ReservaEquipoModel:
     ahora_completo = datetime.now()
     ahora_hora = ahora_completo.time()
     hoy = ahora_completo.date()

     try:
        with self.db.begin():
            dbreservaEquipo = (
                self.db.query(ReservaEquipoModel)
                .filter(ReservaEquipoModel.idReservaEquipo == idReservaEquipo)
                .with_for_update()  
                .first()
            )

            if not dbreservaEquipo:
                return None

            reserva_padre = dbreservaEquipo.reserva

            # Validar que la reserva sea para hoy
            if reserva_padre.fechaReserva != hoy:
                raise ValueError(f"Esta reserva no es para el día de hoy ({hoy}).")

            # Validar que la reserva no haya terminado
            if reserva_padre.horaFin <= ahora_hora:
                raise ValueError(
                    f"La reserva ya terminó a las {reserva_padre.horaFin}. "
                    "No se puede registrar uso después del horario de la reserva."
                )

            if dbreservaEquipo.estadoUso == EstadoUsoEquipo.PENDIENTE:
                # Validar horario de inicio
                if ahora_hora < reserva_padre.horaInicio:
                    raise ValueError(
                        f"Tu reserva comienza a las {reserva_padre.horaInicio}. "
                        "Aún no puedes iniciar el uso."
                    )

                if ahora_hora > reserva_padre.horaFin:
                    raise ValueError(
                        f"Fuera de horario. Tu reserva es de {reserva_padre.horaInicio} a {reserva_padre.horaFin}"
                    )

                # Verificar que nadie más esté usando la máquina
                existe_otro = self.db.query(ReservaEquipoModel).join(ReservaModel).filter(
                    ReservaEquipoModel.equipoId == dbreservaEquipo.equipoId,
                    ReservaEquipoModel.reservaId != dbreservaEquipo.reservaId,
                    ReservaEquipoModel.estadoUso == EstadoUsoEquipo.EN_USO,
                    ReservaModel.fechaReserva == hoy,
                    ReservaModel.horaFin > ahora_hora  # Solo considerar reservas activas
                ).with_for_update().first()

                if existe_otro:
                    raise ValueError("La máquina está siendo usada actualmente por otro usuario.")

                dbreservaEquipo.estadoUso = EstadoUsoEquipo.EN_USO
                dbreservaEquipo.horaInicio = ahora_hora
                dbreservaEquipo.horaFin = None

            elif dbreservaEquipo.estadoUso == EstadoUsoEquipo.EN_USO:
                # Finalizar uso
                dbreservaEquipo.estadoUso = EstadoUsoEquipo.FIN_USO
                dbreservaEquipo.horaFin = ahora_hora

        self.db.refresh(dbreservaEquipo)
        return dbreservaEquipo

     except SQLAlchemyError:
        self.db.rollback()
        raise
    def actualizarEquipoReserva(self, id_reserva_equipo: int, nuevo_equipo_id: int):

        db_re = self.db.query(ReservaEquipoModel).filter(
        ReservaEquipoModel.idReservaEquipo == id_reserva_equipo
        ).first()
        if db_re:
         db_re.equipoId = nuevo_equipo_id
         db_re.estadoUso = EstadoUsoEquipo.PENDIENTE 
         self.db.commit()
         self.db.refresh(db_re)
        return db_re
    
    def cancelarReservasPorRetraso(self):
     ahora = datetime.now()
     limite = ahora - timedelta(minutes=15)
     hoy = ahora.date()
     hora_actual = ahora.time()

    # Buscamos reservas PENDIENTES de hoy que ya pasaron su hora de inicio + 15 min
     reservas_atrasadas = self.db.query(ReservaModel).filter(
        ReservaModel.estado == EstadoReserva.PENDIENTE,
        ReservaModel.fechaReserva == hoy,
        ReservaModel.horaInicio <= limite.time() ).all()

     for reserva in reservas_atrasadas:
        reserva.estado = EstadoReserva.CANCELADO
        reserva.motivoCancelacion = MotivoCancelacion.CANCELACION_POR_RETRASO
    
     self.db.commit()


    def agregarEquipoAReserva(self, id_reserva: int, id_equipo: int) -> ReservaEquipoModel:
        dbReservaEquipo = ReservaEquipoModel(
        estadoUso=EstadoUsoEquipo.PENDIENTE,
        reservaId=id_reserva,
        equipoId=id_equipo)
        self.db.add(dbReservaEquipo)
        self.db.commit()
        self.db.refresh(dbReservaEquipo)
        return dbReservaEquipo
     
    def obtenerReservaPorId(self, id_reserva: int) -> ReservaModel:
        return self.db.query(ReservaModel).filter(ReservaModel.idReserva == id_reserva).first()