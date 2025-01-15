from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from tci.core.config import settings

engine = create_engine(settings.POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
        self.Base = Base

    def get_session(self):
        db = SessionLocal()
        try:
            return db
        finally:
            db.close()


db = Database()
