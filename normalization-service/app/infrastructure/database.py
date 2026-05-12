import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CATALOG_DB_URL = os.getenv("CATALOG_DB_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

catalog_engine = create_engine(CATALOG_DB_URL)
CatalogSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=catalog_engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_catalog_db():
    db = CatalogSessionLocal()
    try:
        yield db
    finally:
        db.close()
