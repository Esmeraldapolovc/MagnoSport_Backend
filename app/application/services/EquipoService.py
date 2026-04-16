from ..interfaces.repository.IEquipoRepository import IEquipoRepository
from ..interfaces.service.IEquipoService import IEquipoService
from ..dtos.equipo import AgregarEquipoDTO, ActualizarEquipoDTO
from app.domain.entities.equipo import Equipo, Categoria, Estado
from datetime import date
class EquipoService(IEquipoService):

    def __init__(self, equipo_repository: IEquipoRepository):
        self.equipo_repository = equipo_repository

    def registrarEquipo(self, dto: AgregarEquipoDTO):

        if dto.categoria == Categoria.MATERIAL:
            if dto.cantidad <= 0:
              raise ValueError("La cantidad debe ser mayor a cero")
        
            cantidad_final = dto.cantidad
        else:
           cantidad_final = 1

        equipo_entidad = Equipo(
        nombre=dto.nombre,
        cantidad=cantidad_final,
        categoria=dto.categoria,
        fechaRegistro=date.today(),
        estado=Estado.DISPONIBLE,
        area=dto.areaId
    )

        resultado = self.equipo_repository.registrarEquipo(equipo_entidad)
    
        return f"{dto.categoria.value} registrado con éxito" if resultado else "Error al registrar"
    
    def actualizarEquipo(self, dto: ActualizarEquipoDTO) -> Equipo:
        if dto.categoria == Categoria.MATERIAL:
            if dto.cantidad is None or dto.cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero")
            
            cantidad_final = dto.cantidad
        else:
            cantidad_final = 1

        equipo_entidad = Equipo(
            idEquipo=dto.idEquipo,
            nombre=dto.nombre,
            cantidad=cantidad_final,
            categoria=dto.categoria,
            fechaRegistro=dto.fechaRegistro,
            estado=dto.estado,
            area=dto.areaId
        )

        resultado = self.equipo_repository.actualizarEquipo(equipo_entidad)

        return f"{dto.categoria.value} actualizado con éxito" if resultado else "Error al actualizar"
    
    def ListadoEquipos(self) -> list[Equipo]:
        
        return self.equipo_repository.ListadoEquipos()
    
    def obtenerEquipoPorNombre(self, nombre: str) -> list[Equipo]:
        return self.equipo_repository.obtenerEquipoPorNombre(nombre)
    
    def obtenerEquipoPorId(self, idEquipo: int) -> Equipo:
        return self.equipo_repository.obtenerEquipoPorId(idEquipo)
    
    def obtenerEquipoGeneralPorNombre(self, nombre: str) -> list[Equipo]:
        return self.equipo_repository.obtenerEquipoGeneralPorNombre(nombre)


