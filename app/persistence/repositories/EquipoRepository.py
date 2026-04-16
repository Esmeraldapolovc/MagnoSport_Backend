from ast import List

from sqlalchemy.orm import Session
from app.domain.entities import Equipo
from app.persistence.models.equipo import Equipo as EquipoModel
from app.persistence.models.enums import CategoriaEquipo, EstadoEquipo, EstadoUsoEquipo
from app.application.interfaces.repository.IEquipoRepository import IEquipoRepository
from sqlalchemy import func, over, case

class EquipoRepository(IEquipoRepository):

    def __init__(self, db: Session):
        self.db = db

    def registrarEquipo(self, equipo: Equipo) -> Equipo:
        dbEquipo = EquipoModel(
                nombre=equipo.nombre,
                cantidad=equipo.cantidad,
                categoria=equipo.categoria.value,
                fechaRegistro=equipo.fechaRegistro,
                estado=equipo.estado.value,
                areaId = equipo.area
            )

        self.db.add(dbEquipo)
        self.db.commit()
        self.db.refresh(dbEquipo)
        return dbEquipo
    
    def actualizarEquipo(self, equipo: Equipo) -> Equipo:
        dbEquipo = self.db.query(EquipoModel).filter(EquipoModel.idEquipo == equipo.idEquipo).first()
        if not dbEquipo:
            return None
        
        dbEquipo.nombre = equipo.nombre
        dbEquipo.cantidad = equipo.cantidad
        dbEquipo.categoria = equipo.categoria.value
        dbEquipo.fechaRegistro = equipo.fechaRegistro
        dbEquipo.estado = equipo.estado.value
        dbEquipo.areaId = equipo.area

        self.db.commit()
        self.db.refresh(dbEquipo)
        return dbEquipo
    
    from sqlalchemy import func, case

    def ListadoEquipos(self):
     prioridad_estados = case(
        (EquipoModel.estado == "Disponible", 1),
        (EquipoModel.estado == "No disponible", 2),
        (EquipoModel.estado == "Mantenimiento", 3),
        (EquipoModel.estado == "Fuera de servicio", 4),
        else_=99 )
    
     subquery = (
        self.db.query(
            EquipoModel.nombre,
            EquipoModel.estado,
            func.row_number().over(
                partition_by=EquipoModel.nombre,
                order_by=prioridad_estados
            ).label('rn')
        )
        .subquery())
    
     estados_prioritarios = (
        self.db.query(subquery.c.nombre, subquery.c.estado)
        .filter(subquery.c.rn == 1)
        .subquery())
    
     equipos_agrupados = (
        self.db.query(
            func.max(EquipoModel.idEquipo).label("idEquipo"),
            EquipoModel.nombre,
            func.sum(EquipoModel.cantidad).label("total_cantidad"),
            EquipoModel.categoria,
            func.max(EquipoModel.fechaRegistro).label("fechaRegistro"),
            estados_prioritarios.c.estado.label("estado_prioritario"),
            EquipoModel.areaId
        )
        .join(
            estados_prioritarios,
            EquipoModel.nombre == estados_prioritarios.c.nombre
        )
        .group_by(
            EquipoModel.nombre,
            EquipoModel.categoria,
            EquipoModel.areaId,
            estados_prioritarios.c.estado
        )
        .all()
    )
    
     return [Equipo(
        idEquipo=e.idEquipo,
        nombre=e.nombre,
        cantidad=e.total_cantidad,
        categoria=CategoriaEquipo(e.categoria),
        fechaRegistro=e.fechaRegistro,
        estado=EstadoEquipo(e.estado_prioritario),
        area=e.areaId
    ) for e in equipos_agrupados]


    def obtenerEquipoPorNombre(self, nombre: str) -> list[Equipo]:
     equipos_db = self.db.query(EquipoModel).filter(EquipoModel.nombre == nombre).all()
    
     if equipos_db:
        return [Equipo(
            idEquipo=e.idEquipo,      
            nombre=e.nombre,
            cantidad=e.cantidad,
            categoria=CategoriaEquipo(e.categoria),
            fechaRegistro=e.fechaRegistro,
            estado=EstadoEquipo(e.estado),
            area=e.areaId
        ) for e in equipos_db]
    
     return [] 

    
    def obtenerEquipoPorId(self, idEquipo: int) -> Equipo:
        equipo = self.db.query(EquipoModel).filter(EquipoModel.idEquipo == idEquipo).first()
        if equipo:
            return Equipo(
                idEquipo=equipo.idEquipo,
                nombre=equipo.nombre,
                cantidad=equipo.cantidad,
                categoria=CategoriaEquipo(equipo.categoria),
                fechaRegistro=equipo.fechaRegistro,
                estado=EstadoEquipo(equipo.estado),
                area=equipo.areaId
            )
        return None
    
    def obtenerEquipoGeneralPorNombre (self, nombre: str) -> list[Equipo]:
        equipos_agrupados = (
        self.db.query(
            func.max(EquipoModel.idEquipo).label("idEquipo"), 
            EquipoModel.nombre,
            func.sum(EquipoModel.cantidad).label("total_cantidad"),
            EquipoModel.categoria,
            func.max(EquipoModel.fechaRegistro).label("fechaRegistro"),
            EquipoModel.estado,
            EquipoModel.areaId
        )
        .filter(EquipoModel.estado == EstadoEquipo.DISPONIBLE, EquipoModel.nombre == nombre)
        .group_by(
            EquipoModel.nombre, 
            EquipoModel.categoria, 
            EquipoModel.areaId, 
            EquipoModel.estado
        )
        .all()
    )

        return [Equipo(
        idEquipo=e.idEquipo,
        nombre=e.nombre,
        cantidad=e.total_cantidad, 
        categoria=CategoriaEquipo(e.categoria),
        fechaRegistro=e.fechaRegistro,
        estado=EstadoEquipo(e.estado),
        area=e.areaId
    ) for e in equipos_agrupados]