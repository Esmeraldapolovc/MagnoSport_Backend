import logging
from app.persistence.models.nivelAcademico import NivelAcademico
from app.infrastructure.database import SessionLocal

logger = logging.getLogger(__name__)


class SeendsNivelAcademico:
    @staticmethod
    def run():
        db = SessionLocal()
        logger.info("Iniciando el proceso de seeding de niveles académicos...")

        niveles_iniciales = ["Bachillerato", "Licenciatura",]

        try:
            for nombre in niveles_iniciales:
                nivel_existente = db.query(NivelAcademico).filter_by(
                    nombreNivel=nombre).first()

                if not nivel_existente:
                    nuevo_nivel = NivelAcademico(nombreNivel=nombre)
                    db.add(nuevo_nivel)
                    db.flush()
                    logger.info(
                        "Nivel académico '%s' agregado exitosamente.", nombre)
                else:
                    logger.warning(
                        "El nivel académico '%s' ya existía. Saltando...", nombre)

            db.commit()
            logger.info("Seeding de niveles académicos completado con éxito.")

        except Exception as e:
            db.rollback()
            logger.error("Error crítico durante el seeding: %s", str(e))
            raise e
        finally:
            db.close()
