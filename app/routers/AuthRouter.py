from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from app.models.UserModel import Token, User, UserCreate
from app.services.AuthService import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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


@router.get("/users/me/", response_model=User)
async def get_current_user(
    authService: Annotated[AuthService, Depends()],
    auth: Annotated[OAuth2PasswordBearer, Depends(oauth2_scheme)],
) -> User:
    return authService.get_current_active_user(auth)
