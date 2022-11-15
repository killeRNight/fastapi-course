"""

Database set up.

"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


SQLALCHEMY_DATABASE_URI = f'postgresql://' \
                          f'{settings.DATABASE_USERNAME}' \
                          f':{settings.DATABASE_PASSWORD}' \
                          f'@{settings.DATABASE_HOSTNAME}' \
                          f':{settings.DATABASE_PORT}' \
                          f'/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
