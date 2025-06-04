from sqlmodel import Session, create_engine
from fastapi import Depends
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def get_db():
    with Session(engine) as session:
        yield session
