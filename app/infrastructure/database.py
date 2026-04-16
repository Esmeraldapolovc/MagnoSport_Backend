from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  # Añade esto
from sqlalchemy.orm import sessionmaker
from app.infrastructure.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
