from sqlalchemy import create_engine
from db.base import Base
from db.models import *
from sqlalchemy.orm import sessionmaker

connection_string = "postgresql://postgres:postgres@localhost:5432/lzdb"
engine = create_engine(connection_string, echo=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()