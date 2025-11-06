from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import Config
from .models import Base

engine = create_engine(Config.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)

