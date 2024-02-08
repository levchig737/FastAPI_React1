from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_URL = "postgresql://postgres:pass@localhost/postgres"

engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Получает сессию/бд
    :return: сессию/бд
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
