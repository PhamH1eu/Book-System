from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from app.models.UserModel import Token, TokenData, User, UserCreate
from app.services.AuthService import AuthService

router = APIRouter(tags=["security"])


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authService: Annotated[AuthService, Depends()],
) -> Token:
    return authService.sign_in(form_data)


@router.post("/register")
async def register(
    user: UserCreate, authService: Annotated[AuthService, Depends()]
) -> User:
    return authService.create_user(user)


@router.get("/users/me/")
async def get_current_user(
    current_user: Annotated[TokenData, Depends(AuthService().get_current_user)],
) -> User:
    return current_user
