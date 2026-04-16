from typing import Generator
from sqlalchemy.orm import Session
from app.application.services.LicenciaturaService import  LicenciaturaService
from app.application.services.EquipoService import EquipoService
from app.infrastructure.database import SessionLocal
from app.persistence.repositories.AsistenciasyReservasRpository import AsistenciasyReservasRepository
from app.persistence.repositories.usuarioRepository import UsuarioRepository
from app.persistence.repositories.rolRepository import RolRepository
from app.persistence.repositories import DashboardRepository, HorarioRepository
from app.persistence.repositories.licenciaturaRepository import LicenciaturaRepository
from app.persistence.repositories.nivelAcademicoRepository import NivelAcademicoRepository
from app.persistence.repositories.ReservaRepository import ReservaRepository
from app.persistence.repositories.AreaRepository import AreaRepository
from app.persistence.repositories.EquipoRepository import EquipoRepository
from app.persistence.repositories.DashboardRepository import DashboardRepository
from app.application.services.DashboardService import DashboardService
from app.application.services.NivelService import NivelService
from app.application.services.usuarioService import UsuarioService
from app.application.services.HorarioService import HorarioService
from app.application.services.ReservaService import ReservaService
from app.application.services.NoticiaService import NoticiaService
from app.application.services.AsistenciasyReservasService import AsistenciasyReservasService
from app.persistence.repositories.NoticiasRepository import NoticiasRepository

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.jwt_manager import verify_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    return payload

def require_admin(usuario = Depends(get_current_user)):

    if usuario["rol"] != 1:
        raise HTTPException(status_code=403, detail="Solo administradores")

    return usuario

def get_db() -> Generator:
    """
    Crea una nueva sesión de base de datos para cada petición
    y la cierra automáticamente al terminar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_usuario_service(db: Session = Depends(get_db)):
    repository = UsuarioRepository(db)
    repositoryRol = RolRepository(db)
    repositoryNivel = NivelAcademicoRepository(db)
    repositoryLic   = LicenciaturaRepository(db)

    return UsuarioService(repository, repositoryRol, repositoryNivel, repositoryLic)

def get_horario_service(db: Session = Depends(get_db)):
    repositoryHorario = HorarioRepository(db)

    return HorarioService(repositoryHorario)

def get_reserva_service(db: Session = Depends(get_db)):
    repositoryReserva = ReservaRepository(db)
    repositoryArea = AreaRepository(db)
    repositoryHorario = HorarioRepository(db)
    repository = UsuarioRepository(db)
    repositoryEquipo = EquipoRepository(db)

    return ReservaService(repositoryReserva,repositoryHorario ,repositoryArea, repository, repositoryEquipo)

def get_asistenciasyreservas_service(db: Session = Depends(get_db)):
    repository = AsistenciasyReservasRepository(db)
    repositoryReserva = ReservaRepository(db)

    return AsistenciasyReservasService(repository, repositoryReserva)


def get_Noticia_service(db: Session = Depends(get_db)):
    repository = NoticiasRepository(db)
   
    
    return NoticiaService(repository)

def get_equipo_service(db: Session = Depends(get_db)):
    repository = EquipoRepository(db)
    
    return EquipoService(repository)

def get_licenciatura_service(db: Session = Depends(get_db)):
    repository = LicenciaturaRepository(db)
    
    return LicenciaturaService(repository)

def get_nivel_service(db: Session = Depends(get_db)):
    repository = NivelAcademicoRepository(db)

    return NivelService(repository)

def get_dashboard_service(db: Session = Depends(get_db)):
    repository = DashboardRepository(db)

    return DashboardService(repository)