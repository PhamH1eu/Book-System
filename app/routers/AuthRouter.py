from typing_extensions import Annotated
from fastapi import APIRouter, Depends


from app.models.UserModel import Token, User
from app.services.AuthService import validate_token_middleware, sign_in, create_user, refresh_token, logout

router = APIRouter(tags=["security"])


@router.post("/token")
def login(sign_in_response: Annotated[Token, Depends(sign_in)]) -> Token:
    return sign_in_response

@router.get("/refresh")
async def refresh_access_token(new_access_token: Annotated[Token, Depends(refresh_token)]) -> Token:
    return new_access_token

@router.post("/register")
def register(user_response: Annotated[User, Depends(create_user)]) -> User:
    return user_response


@router.get("/users/me/")
def get_current_user(current_user: Annotated[str, Depends(validate_token_middleware)]):
    return current_user

@router.get("/logout")
def log_out(response = Depends(logout)):
    return response
