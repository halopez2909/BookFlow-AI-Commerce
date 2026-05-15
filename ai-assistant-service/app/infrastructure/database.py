"""
Configuración SQLAlchemy. Define el engine, la SessionLocal y la
función create_tables() que el main.py invoca al arrancar.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://bookflow:bookflow123@postgres:5432/assistant_db",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def get_db():
    """Dependency de FastAPI: yielda una sesión y la cierra al final."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """
    Crea las tablas si no existen. Útil en desarrollo / docker-compose.
    En producción se usa Alembic.
    """
    # Importar aquí para que Base.metadata vea los modelos antes de create_all
    from app.infrastructure import models  # noqa: F401
    Base.metadata.create_all(bind=engine)