from app.routers import AuthorRouter, BookRouter, AuthRouter
from app.configs.Database import create_app

app = create_app()

app.include_router(AuthRouter.router)
app.include_router(AuthorRouter.router)
app.include_router(BookRouter.router)
