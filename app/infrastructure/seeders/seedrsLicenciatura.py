import logging
from app.persistence.models.licenciatura import Licenciatura
from app.infrastructure.database import SessionLocal


logger = logging.getLogger(__name__)


class SeedrsLicenciatura:
    @staticmethod
    def run():
        db = SessionLocal()
        logger.info("Iniciando el proceso de seeding de Licenciaturas...")

        licenciatura = ["Entrenamiento Deportivo", "Finanzas y Contabilidad", "Psicopedagogía", "Administración de Negocios", "Fisoterapia"]
        NIVEL_LICENCIATURA = 2

        try:
            for nombre in licenciatura:
                licenciatura_existentes = db.query(
                    Licenciatura).filter_by(nombreLic=nombre).first()

                if not licenciatura_existentes:
                    nuevalic = Licenciatura(nombreLic=nombre, nivelId=NIVEL_LICENCIATURA)
                    db.add(nuevalic)
                    db.flush()
                    logger.info(
                        "La Licenciatura fue '%s' agregado exitosamente.", nombre)
                else:
                    logger.warning(
                        "La Licenciatura '%s'  ya existia. Saltando...", nombre)
            db.commit()
            logger.info("Seeding de Licenciatura completado con éxito")
        except Exception as e:
            db.rollback()
            logger.error("Error crítico durante el seeding: %s", str(e))
            raise e
        finally:
            db.close()

