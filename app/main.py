from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from db.constants import DATABASE_URL
from db.db_operations import *
from fastapi import FastAPI
from api.endpoints import router
import uvicorn

if __name__=="__main__":
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    preload_exercise_names(SessionLocal())
    
    app = FastAPI()
    app.include_router(router, prefix="")
    uvicorn.run(app, host="127.0.0.1", port=8000)