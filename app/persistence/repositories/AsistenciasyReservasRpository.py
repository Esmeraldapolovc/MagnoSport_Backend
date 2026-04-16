from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from app.application.dtos.reserva.reservaDTO import ReservaDetalleDTO
from app.application.interfaces.repository.IAsistenciasyReservasRepository import IAsistenciasyReservasRepository
from app.persistence.models.horario import Horario as HorarioModel
from app.persistence.models.reserva import Reserva as ReservaModel
from app.persistence.models.usuario import Usuario as UsuarioModel
from app.persistence.models.dia import Dia as DiaModel
from app.persistence.models.area import Area as AreaModel
from app.persistence.models.excepcionHorario import ExcepcionHorario as ExcepcionHorarioModel
from app.persistence.models.alumno import Alumno as AlumnoModel
from app.persistence.models.reservaEquipo import ReservaEquipo as ReservaEquipoModel
from app.persistence.models.reservaLaboral import ReservaLaboral as ReservaLaboralModel
from app.domain.entities.usuario import Usuario
from app.domain.entities import Alumno, Reserva as ReservaEntidad, reserva
from app.persistence.models.enums import EstadoReserva

class AsistenciasyReservasRepository(IAsistenciasyReservasRepository):
    def __init__(self, db: Session):
        self.db = db

    def obtenerHorariosAsistenciasyReservas(self, idArea: int):
    
     return (
        self.db.query(HorarioModel)
        .options(
            joinedload(HorarioModel.dias),
            joinedload(HorarioModel.excepciones),
            joinedload(HorarioModel.reservas)
            .joinedload(ReservaModel.usuario)
            .joinedload(UsuarioModel.rol)
        )
        .all()
    )


    def detallesUsuarioReserva(self, idReserva: int) :
     dbReserva = (
     self.db.query(ReservaModel)
        .options(
        joinedload(ReservaModel.usuario).joinedload(UsuarioModel.alumno).joinedload(AlumnoModel.nivel),
        joinedload(ReservaModel.usuario).joinedload(UsuarioModel.alumno).joinedload(AlumnoModel.licenciatura),
        # Cambia el joinedload para asegurar que use el nombre de la relación en el modelo
        joinedload(ReservaModel.reserva_equipos).joinedload(ReservaEquipoModel.equipo),
        joinedload(ReservaModel.reserva_laboral).joinedload(ReservaLaboralModel.licenciatura) 
     )
     .filter(ReservaModel.idReserva == idReserva)
     .first())

     if not dbReserva:
        return None

     dbUsuario = dbReserva.usuario
     usuario_entidad = None

    #  Mapeo: Determinar si el usuario es Alumno o Usuario base
     if dbUsuario.alumno:
        # Creamos la Entidad de Dominio Alumno
        usuario_entidad = Alumno(
            idUsuario=dbUsuario.idUsuario,
            nombre=dbUsuario.nombre,
            correo=dbUsuario.correo,
            foto=dbUsuario.foto,
            estatus=dbUsuario.estatus,
            rol=dbUsuario.rol,
            # Datos de Alumno
            fechaInicio=dbUsuario.alumno.fechaInicio,
            fechaFin=dbUsuario.alumno.fechaFin,
            nivel=dbUsuario.alumno.nivel, 
            licenciatura=dbUsuario.alumno.licenciatura,
            contrasenia=None
        )
     else:
        # Creamos la Entidad de Dominio Usuario base
        usuario_entidad = Usuario(
            idUsuario=dbUsuario.idUsuario,
            nombre=dbUsuario.nombre,
            correo=dbUsuario.correo,
            foto=dbUsuario.foto,
            estatus=dbUsuario.estatus,
            rol=dbUsuario.rol,
            contrasenia=None
        )

   
    
     return ReservaDetalleDTO(
        idReserva=dbReserva.idReserva,
        areaId=dbReserva.areaId,
        estado=dbReserva.estado,
        usuario=usuario_entidad,
        reserva_equipos=dbReserva.reserva_equipos,
        reserva_laboral=dbReserva.reserva_laboral,
        tipo_reserva=dbReserva.tipoReserva)
     
       
    def registrarAsistencia(self, idReserva:int):
     reserva = self.db.query(ReservaModel).filter(ReservaModel.idReserva == idReserva).first()
    
     if not reserva:
        raise ValueError("Reserva no encontrada")

   
     if reserva.estado == EstadoReserva.CANCELADO: 
        raise ValueError("No se puede registrar asistencia para una reserva cancelada")
    
     if reserva.estado == EstadoReserva.ASISTIO:
        raise ValueError("La asistencia ya ha sido registrada anteriormente")

     if reserva.estado == EstadoReserva.PENDIENTE:
        reserva.estado = EstadoReserva.ASISTIO

     try:
        self.db.commit()
        self.db.refresh(reserva)
        return True
     except Exception as e:
        self.db.rollback()
        raise e
     
    def obtenerReservaPorId(self, idReserva: int):
     return self.db.query(ReservaModel).filter(ReservaModel.idReserva == idReserva).first()
       
        

   