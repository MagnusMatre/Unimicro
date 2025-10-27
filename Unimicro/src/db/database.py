from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from . import tables
DATABASE_URL = "postgresql://todo_user:todo_pass@localhost:5432/todo_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def init_db():
    #tables.Task.__table__.drop(bind=engine, checkfirst=True)
    Base.metadata.create_all(bind=engine)

def close_db():
    pass