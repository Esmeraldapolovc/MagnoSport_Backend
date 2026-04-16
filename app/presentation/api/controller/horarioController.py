from fastapi import HTTPException
from app.application.interfaces.service.IHorarioService import IHorarioService
from app.application.dtos.horario import HorarioCreateDTO, ExcepcionCreateDTO
from ...schemas.HorarioSchemas import HorarioCreateSchema, ExcepcionSchema
from datetime import date

class HorarioController:
    def __init__(self,service: IHorarioService):
        self.service = service


    ########
    def crearHorario(self, request: HorarioCreateSchema):
        try:
            dto = HorarioCreateDTO(
                fechaInicio=request.fechaInicio,
                fechaFin = request.fechaFin,
                horaInicio=request.horaInicio,
                horaFin=request.horaFin,
                dias = request.dias,
                estado=request.estado
            )
            
            return self.service.crearHorario(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def listarHorarios(self):
        try:
            return self.service.listarHorarios()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def crearExcepcion(self, request: ExcepcionSchema):
        try:
            dto = ExcepcionCreateDTO(
                     horarioId=request.horarioId,
            fechaInicio=request.fechaInicio,
            fechaFin=request.fechaFin,
            horaInicio=request.horaInicio,
            horaFin=request.horaFin,
            estado=request.estado
            )

            return self.service.crearExcepcion(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) 
        
    def consultarFecha(self, fecha: date):
        try:
            resultado = self.service.obtenerEstadoPorFecha(fecha)
            return resultado
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    