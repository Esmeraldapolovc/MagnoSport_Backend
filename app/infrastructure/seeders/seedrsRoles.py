import logging
from app.persistence.models.rol import Rol as RolModel
from app.infrastructure.database import SessionLocal

logger = logging.getLogger(__name__)


class SeedsRoles:
    @staticmethod
    def run():
        db = SessionLocal()
        logger.info("Iniciando el proceso de seeding de roles...")

        roles_iniciales = ["Administrador",
                           "Alumno", "Profesor", "Personal"]

        try:
            for nombre in roles_iniciales:
                rol_existente = db.query(RolModel).filter_by(
                    nombreRol=nombre).first()

                if not rol_existente:
                    nuevo_rol = RolModel(nombreRol=nombre)
                    db.add(nuevo_rol)
                    db.flush()
                    logger.info("Rol '%s' agregado exitosamente.", nombre)
                else:
                    # USA COMA, NO F-STRING:
                    logger.warning(
                        " El rol '%s' ya existía. Saltando...", nombre)

            db.commit()
            logger.info(" Seeding de roles completado con éxito.")

        except Exception as e:
            db.rollback()
            # Para excepciones, es mejor pasar el objeto 'e' o usar logger.exception
            logger.error(" Error crítico durante el seeding: %s", str(e))
            raise e
        finally:
            db.close()
