from fastapi import HTTPException
from app.application.dtos.equipo import AgregarEquipoDTO
from app.application.dtos.equipo.actualizarEquipoDTO import ActualizarEquipoDTO
from app.application.interfaces.service.IEquipoService import IEquipoService
from app.presentation.schemas.equipo import AgregarEquipoSchema, ActualizarEquipoSchema


class EquipoController:
    def __init__(self, service: IEquipoService):
        self.service = service

    def registrarEquipo(self, request: AgregarEquipoSchema):
        try:
            dto = AgregarEquipoDTO(
                nombre=request.nombre,
                cantidad=request.cantidad,
                categoria=request.categoria,
                areaId=request.areaId
            )
            return self.service.registrarEquipo(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def actualizarEquipo(self, request: ActualizarEquipoSchema):
        try:
            dto = ActualizarEquipoDTO(
                idEquipo=request.idEquipo,
                nombre=request.nombre,
                cantidad=request.cantidad,
                categoria=request.categoria,
                fechaRegistro=request.fechaRegistro,
                estado=request.estado,
                areaId=request.areaId
            )
            return self.service.actualizarEquipo(dto)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def ListadoEquipos(self):
        try:
          return self.service.ListadoEquipos()
        except ValueError as e:
          raise HTTPException(status_code=400, detail=str(e))
        
    def obtenerEquipoPorNombre(self, nombre: str):
        try:
          return self.service.obtenerEquipoPorNombre(nombre)
        except ValueError as e:
          raise HTTPException(status_code=400, detail=str(e))
        

    def obtenerEquipoPorId(self, idEquipo: int):
        try:
          return self.service.obtenerEquipoPorId(idEquipo)
        except ValueError as e:
          raise HTTPException(status_code=400, detail=str(e))
        
    def obtenerEquipoGeneralPorNombre(self, nombre: str):
        try:
          return self.service.obtenerEquipoGeneralPorNombre(nombre)
        except ValueError as e:
          raise HTTPException(status_code=400, detail=str(e))