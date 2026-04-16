import os
from dotenv import load_dotenv
from pathlib import Path

# Localiza el archivo .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "MAGNOSport API"
    PROJECT_VERSION: str = "1.0.0"

    # Extraer valores del entorno
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "MAGNOSport")

    # Construir la URL usando las variables ya extraídas
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_super_secreta_123")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
