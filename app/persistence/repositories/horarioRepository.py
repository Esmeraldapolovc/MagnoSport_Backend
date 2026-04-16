from operator import and_

from app.application.interfaces.repository.IHorarioRepository import IHorarioRepository
from app.persistence.models.horario import Horario as HorarioModel
from app.persistence.models.horarioDia import HorarioDia as HorarioDiaModel
from app.persistence.models.excepcionHorario import ExcepcionHorario as ExcepcionModel
from app.domain.entities import Horario, HorarioDia, ExcepcionHorario
from app.persistence.models.reserva import Reserva as ReservaModel
from app.persistence.models.enums import EstadoReserva, MotivoCancelacion, EstadoExcepcion
from app.persistence.models.enums import EstadoHorario
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date


class HorarioRepository(IHorarioRepository):
    def __init__(self, db: Session):
        self.db = db

    def verificarSolapamiento(self, fechaInicio, fechaFin, horaInicio, horaFin, diasIds: List[int]) -> bool:
    # 1. Filtramos por los días que estamos intentando registrar
    # 2. Filtramos por solapamiento de fechas calendario
    # 3. Filtramos por solapamiento de horas
        query = self.db.query(HorarioModel).join(HorarioModel.dias).filter(
        HorarioDiaModel.diaId.in_(diasIds),
        HorarioModel.fechaInicio <= fechaFin,
        HorarioModel.fechaFin >= fechaInicio,
        HorarioModel.horaInicio < horaFin,
        HorarioModel.horaFin > horaInicio
    )
    
        return query.first() is not None

    def crearHorario(self, horario: Horario, dias_ids: List[int]) -> Horario:
        db_horario = HorarioModel(
        fechaInicio=horario.fechaInicio,
        fechaFin=horario.fechaFin,
        horaInicio=horario.horaInicio,
        horaFin=horario.horaFin,
        estado=horario.estado
        )
        self.db.add(db_horario)
        self.db.flush()

        for dia_id in dias_ids:
            db_horario_dia = HorarioDiaModel(
            diaId=dia_id,
            horarioId=db_horario.idHorario
            )
            self.db.add(db_horario_dia)

        self.db.commit()
        self.db.refresh(db_horario) 
    
        horario.idHorario = db_horario.idHorario
        return horario
    
    def obtenerPorId(self, id: int):
       return self.db.query(HorarioModel).filter(HorarioModel.idHorario == id).first()

    def crearExcepcion(self, entidad: ExcepcionHorario) -> ExcepcionModel:
     # 1. Crear la instancia en la base de datos
     db_excepcion = ExcepcionModel(
        horarioId=entidad.horario,
        fechaInicio=entidad.fechaInicio,
        fechaFin=entidad.fechaFin,
        horaInicio=entidad.horaInicio,
        horaFin=entidad.horaFin,
        estado=entidad.estado)
     self.db.add(db_excepcion)
    
    # 2. Lógica de cancelación
     estado_exce_val = entidad.estado.value if hasattr(entidad.estado, 'value') else entidad.estado
    
     if str(estado_exce_val).upper() == "CERRADO":
        # Nota: Eliminamos and_() y pasamos las condiciones directamente a filter()
        self.db.query(ReservaModel).filter(
            ReservaModel.horarioId == entidad.horario,
            ReservaModel.fechaReserva >= entidad.fechaInicio,
            ReservaModel.fechaReserva <= entidad.fechaFin,
            ReservaModel.horaInicio >= entidad.horaInicio,
            ReservaModel.horaInicio < entidad.horaFin,
            ReservaModel.estado.in_([EstadoReserva.PENDIENTE, "PENDIENTE"])
        ).update({
            ReservaModel.estado: EstadoReserva.CANCELADO,
            ReservaModel.motivoCancelacion: MotivoCancelacion.CANCELACION_POR_EXCEPCION
        }, synchronize_session=False)

     self.db.commit()
     self.db.refresh(db_excepcion)
     entidad.idExcepcion = db_excepcion.idExcepcion
     return entidad
    
    def listarHorarios(self) -> List[HorarioModel]:
        return self.db.query(HorarioModel)\
            .options(joinedload(HorarioModel.dias),
                     joinedload(HorarioModel.excepciones))\
            .all()
    
    def buscarPorFecha(self, fecha: date) -> List[HorarioModel]:  # Cambiar a List
     dia_semana = fecha.weekday() + 1
     return self.db.query(HorarioModel)\
        .join(HorarioModel.dias)\
        .filter(
            HorarioModel.fechaInicio <= fecha,
            HorarioModel.fechaFin >= fecha,
            HorarioDiaModel.diaId == dia_semana  
        )\
        .options(
            joinedload(HorarioModel.excepciones), 
            joinedload(HorarioModel.dias)
        )\
        .all()
    
    def obtenerExcepcionesPorHorario(self, horario_id: int) -> List[ExcepcionModel]:
     return self.db.query(ExcepcionModel)\
        .filter(ExcepcionModel.horarioId == horario_id)\
        .all()
    
    
    
  