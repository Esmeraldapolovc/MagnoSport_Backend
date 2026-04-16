import sys
from app.infrastructure.logging_config import setup_logging
from app.infrastructure.seeders.seedrsRoles import SeedsRoles
from app.infrastructure.seeders.seedrsNivelAcademico import SeendsNivelAcademico
from app.infrastructure.seeders.seedrsDias import SeedsDias
from app.infrastructure.seeders.seedrsArea import SeedsArea
from app.infrastructure.seeders.seedrsLicenciatura import SeedrsLicenciatura
from app.infrastructure.seeders.seedrsAdministrador import SeedsAdministrador
# Cargamos la configuración de logs para ver los mensajes en consola
setup_logging()


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "seed":
            print("--- Iniciando proceso de carga ---")
            SeedsRoles.run()
            SeendsNivelAcademico.run()
            SeedsDias.run()
            SeedsArea.run()
            SeedrsLicenciatura.run()
            SeedsAdministrador.run()

            print("--- Proceso terminado ---")
        else:
            print(f"Comando '{command}' no reconocido.")
    else:
        print("Uso: python manage.py seed")


if __name__ == "__main__":
    main()
