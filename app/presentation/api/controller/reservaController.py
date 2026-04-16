from datetime import date

from fastapi import HTTPException
from app.application.dtos.reserva.reservaEquipoDTO import ReservaEquipoDTO
from app.application.interfaces.service.IReservaService import IReservaService
from app.application.dtos.reserva import ReservaAlumnoCreateDTO, ObtenerAgendaDTO, ReservaDeleteDTO, ReservaDetailsDTO, EstadoUsoUpdateDTO
from app.presentation.schemas.reserva.reservaEquipoSchema import ReservaEquipoSchema
from ...schemas.reserva import ReservaAlumno1Schemas, ReservaIdShemas, ReservaDeleteSchemas, EstadoUsoUpdateSchema, ReservaAdmin1Schemas

class ReservaController:
    def __init__(self, service : IReservaService):
        self.service = service

    def reservaUsuario1 (self, request: ReservaAlumno1Schemas, usuarioId: int):
        try:
            dto = ReservaAlumnoCreateDTO(
                fechaReserva=request.fechaReserva,
                horaInicio=request.horaInicio,
                horaFin=request.horaFin,
                areaId=request.areaId,
                usuarioId=usuarioId,
                horarioId=request.horarioId,
                tipoReserva=request.tipoReserva,
                claseImpartir=request.claseImpartir,
                licId=request.licId,
                equipoId = request.equipoId
            )

            return self.service.reservaUsuario1(dto)

        except ValueError as e :
            raise HTTPException(status_code=400, detail=str(e))
        

    def reservaUsuario2 (self, request: ReservaAdmin1Schemas):
        try:
            dto = ReservaAlumnoCreateDTO(
                
                fechaReserva=request.fechaReserva,
                horaInicio=request.horaInicio,
                horaFin=request.horaFin,
                areaId=request.areaId,
                usuarioId=request.idUsuario,
                horarioId=request.horarioId,
                tipoReserva=request.tipoReserva,
                claseImpartir=request.claseImpartir,
                licId=request.licId,
                equipoId = request.equipoId
            )

            return self.service.reservaUsuario1(dto)

        except ValueError as e :
            raise HTTPException(status_code=400, detail=str(e))
        
        
    def obtenerAgendaSemanaActual(self, usuarioId: int):
        try:
            dto = ObtenerAgendaDTO(
                usuarioId=usuarioId
            )
            return self.service.obtenerAgendaRangoUsuario(dto)
        
        except ValueError as e:
            raise HTTPException(status_code=400, detail= str(e))
        
    def cancelarReserva(self, request: ReservaDeleteSchemas, usuarioId):
        try:
            dto = ReservaDeleteDTO(
                idReserva=request.idReserva,
                usuarioId= usuarioId
            )

            return self.service.cancelarReserva(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def detalleReserva(self, idReserva):
        try:
            dto = ReservaDetailsDTO(
                idReserva=idReserva
            )

            return self.service.detalleReserva(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def registrarUsoEquipo(self, request: EstadoUsoUpdateSchema):
        try:
            dto = EstadoUsoUpdateDTO(
                idReservaEquipo=request.idReservaEquipo
            )

            return self.service.cambiarEstadoEquipo(dto)
        
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def buscarHorario(self, fecha: date, usuarioId: int):
        try:
            dto = ObtenerAgendaDTO(
                usuarioId=usuarioId
            )
            return self.service.buscarHorario(fecha, dto)
        
        except ValueError as e:
            raise HTTPException(status_code=400, detail= str(e))
        
    def agregarEquipoAdicional(self, request: ReservaEquipoSchema):
        try:
            dto = ReservaEquipoDTO(
                id_reserva=request.id_reserva,
                id_equipo=request.id_equipo
            )
            return self.service.agregarEquipoAdicional(dto)
        
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))