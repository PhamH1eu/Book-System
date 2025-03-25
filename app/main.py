from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import AuthorRouter, BookRouter
from app.configs.Database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run before the application starts
    create_db_and_tables()
    yield
    # Shutdown: Run after the application shuts down
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(AuthorRouter.router)
app.include_router(BookRouter.router)