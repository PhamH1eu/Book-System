from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine

from .Environment import get_environment_variables

# Runtime Environment Configuration
env = get_environment_variables()

# Generate Database URL
DATABASE_URL = f"{env.DATABASE_DIALECT}://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}@{env.DATABASE_HOSTNAME}/{env.DATABASE_NAME}?sslmode=require"
print(DATABASE_URL)
# DATABASE_URL = "sqlite:///./database.db"

# Create Database Engine
Engine = create_engine(DATABASE_URL, echo=env.DEBUG_MODE, future=True)


def get_session():
    with Session(Engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(Engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run before the application starts
    create_db_and_tables()
    yield
    # Shutdown: Run after the application shuts down
    print("Application shutdown")


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.dependency_overrides[Session] = get_session()
    return app
