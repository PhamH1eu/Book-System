from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from app.models.UserModel import Token, User, UserCreate
from app.services.AuthService import AuthService, validate_token

router = APIRouter(tags=["security"])


@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authService: Annotated[AuthService, Depends()],
) -> Token:
    return authService.sign_in(form_data)


@router.post("/register")
def register(
    user: UserCreate, authService: Annotated[AuthService, Depends()]
) -> User:
    return authService.create_user(user)


@router.get("/users/me/")
def get_current_user(current_user: Annotated[str, Depends(validate_token)]):
    return current_user
