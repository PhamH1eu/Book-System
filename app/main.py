from app.routers import AuthorRouter, BookRouter
from app.configs.Database import create_app

app = create_app()

app.include_router(AuthorRouter.router)
app.include_router(BookRouter.router)