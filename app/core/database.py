from app.core.utils.logging import AppLogger
from app.core import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


global_settings = config.get_settings()
logger = AppLogger.__call__().get_logger()

engine = create_engine(global_settings.postgres_url.unicode_string())
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
