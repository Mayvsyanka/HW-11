"""Module for connection to database"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    The get_db function opens a new database connection if there is none yet for the current application context.
    It will also create the database tables if they do not exist yet.
    
    :return: A context manager that provides a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
