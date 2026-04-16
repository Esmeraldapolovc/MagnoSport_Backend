import logging
from app.persistence.models.dia import Dia
from app.infrastructure.database import SessionLocal

logger = logging.getLogger(__name__)


class SeedsDias:
    @staticmethod
    def run():
        db = SessionLocal()
        logger.info("Iniciando el proceso de seeding de días...")

        dias_iniciales = ["Lunes", "Martes", "Miércoles",
                          "Jueves", "Viernes", "Sábado", "Domingo"]

        try:
            for nombre in dias_iniciales:
                dia_existente = db.query(Dia).filter_by(
                    nombreDia=nombre).first()

                if not dia_existente:
                    nuevo_dia = Dia(nombreDia=nombre)
                    db.add(nuevo_dia)
                    db.flush()
                    logger.info("Día '%s' agregado exitosamente.", nombre)
                else:
                    logger.warning(
                        "El día '%s' ya existía. Saltando...", nombre)

            db.commit()
            logger.info("Seeding de días completado con éxito.")

        except Exception as e:
            db.rollback()
            logger.error("Error crítico durante el seeding: %s", str(e))
            raise e
        finally:
            db.close()
