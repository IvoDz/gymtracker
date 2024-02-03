from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from db.constants import DATABASE_URL
from db.db_operations import *

if __name__=="__main__":
    app = FastAPI()

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    preload_exercise_names(SessionLocal())

    add_set(SessionLocal(), 1, 100, 10)