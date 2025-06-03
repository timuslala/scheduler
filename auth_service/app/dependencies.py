from sqlmodel import Session, create_engine
from fastapi import Depends

DATABASE_URL = "postgresql://user:password@db:5432/scheduling"
engine = create_engine(DATABASE_URL)


def get_db():
    with Session(engine) as session:
        yield session
