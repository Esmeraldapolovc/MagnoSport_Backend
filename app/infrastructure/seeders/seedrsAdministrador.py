import logging
from app.persistence.models.usuario import Usuario
from app.infrastructure.database import SessionLocal
from passlib.context import CryptContext 

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SeedsAdministrador:
    @staticmethod
    def run():
        db = SessionLocal()
        logger.info("Iniciando el proceso de seeding del Administrador...")

        admin_data = {
            "nombre": "Administrador",
            "correo": "admin@gmail.com",
            "contrasenia": "Admin&123*", 
            "rolId": 1, 
            "foto": None,
            "estatus": 1
        }

        try:
            # 1. Verificar si el usuario ya existe por correo
            usuario_existente = db.query(Usuario).filter_by(
                correo=admin_data["correo"]
            ).first()

            if not usuario_existente:
                hashed_password = pwd_context.hash(admin_data["contrasenia"])
                
                nuevo_admin = Usuario(
                    nombre=admin_data["nombre"],
                    correo=admin_data["correo"],
                    contrasenia=hashed_password,
                    foto=admin_data["foto"],
                    estatus=admin_data["estatus"],
                    rolId=admin_data["rolId"]
                )

                db.add(nuevo_admin)
                db.flush()
                
                logger.info("Administrador '%s' creado exitosamente.", admin_data["correo"])
            else:
                logger.warning("El administrador con correo '%s' ya existe. Saltando...", admin_data["correo"])

            db.commit()
            logger.info("Seeding de administrador completado.")

        except Exception as e:
            db.rollback()
            logger.error("Error crítico durante el seeding de administrador: %s", str(e))
            raise e
        finally:
            db.close()