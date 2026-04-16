import logging
from app.persistence.models.area import Area
from app.infrastructure.database import SessionLocal

logger = logging.getLogger(__name__)


class SeedsArea:
    @staticmethod
    def run():
        db = SessionLocal()
        logger.info("Iniciando el proceso de seeding de áreas...")

        areas_iniciales = ["Gimnasio", "Cardio", "TRX",
                           "CanchaBolada", "Cancha de Tenis"]

        try:
            for nombre in areas_iniciales:
                area_existente = db.query(Area).filter_by(
                    nombreArea=nombre).first()

                if not area_existente:
                    nueva_area = Area(nombreArea=nombre)
                    db.add(nueva_area)
                    db.flush()
                    logger.info("Área '%s' agregada exitosamente.", nombre)
                else:
                    logger.warning(
                        "El área '%s' ya existía. Saltando...", nombre)

            db.commit()
            logger.info("Seeding de áreas completado con éxito.")

        except Exception as e:
            db.rollback()
            logger.error("Error crítico durante el seeding: %s", str(e))
            raise e
        finally:
            db.close()
