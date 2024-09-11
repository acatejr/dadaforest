# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# POSTGRES_USER = os.environ.get("POSTGRES_USER")
# POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
# POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
# POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE")

DATABASE_URI = os.environ.get("DATABASE_URI")

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()