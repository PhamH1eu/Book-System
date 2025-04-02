from fastapi.responses import JSONResponse

from app.configs.Database import create_app
from app.exceptions import CustomException
from app.routers import AuthorRouter, AuthRouter, BookRouter

app = create_app()


@app.exception_handler(CustomException)
async def custom_exception_handler(_, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


app.include_router(AuthRouter.router)
app.include_router(AuthorRouter.router)
app.include_router(BookRouter.router)
