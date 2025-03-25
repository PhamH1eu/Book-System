from typing_extensions import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from .Environment import get_environment_variables

# Runtime Environment Configuration
env = get_environment_variables()

# Generate Database URL
# DATABASE_URL = f"{env.DATABASE_DIALECT}://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}@{env.DATABASE_HOSTNAME}:{env.DATABASE_PORT}/{env.DATABASE_NAME}"

DATABASE_URL = f"sqlite:///./database.db"

# Create Database Engine
Engine = create_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)

def get_session():
    with Session(Engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(Engine)

SessionDep = Annotated[Session, Depends(get_session)]