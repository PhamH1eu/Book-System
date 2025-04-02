from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from redis import Redis

from app.configs.Environment import get_environment_variables
from app.configs.redis import get_redis
from app.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    ResourceAlreadyExistsException,
    UnauthorizedException,
)
from app.models.UserModel import Token, UserCreate, UserInDB
from app.repositories.UserRepo import UserRepository

env = get_environment_variables()
SECRET_KEY = env.SECRET_KEY
ALGORITHM = env.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(env.ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE_DAYS = int(env.REFRESH_TOKEN_EXPIRE_DAYS)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        password=plain_password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )


def get_password_hash(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "token_type": TokenType.ACCESS})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "token_type": TokenType.REFRESH})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def blacklist_tokens(access_token, redis: Redis) -> None:
    username = decode_token(access_token)
    redis.set(f"TOKEN_BLACK_LIST_{username}", 1, ex=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def is_token_blacklisted(token: str, redis: Redis) -> bool:
    username = decode_token(token)
    if redis.exists(f"TOKEN_BLACK_LIST_{username}"):
        return True
    return False


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        print(username)
        if username is None:
            raise InvalidTokenException("Could not validate credentials")
    except InvalidTokenError:
        raise InvalidTokenException("Could not validate credentials")
    return username


def validate_token_middleware(
    token: Annotated[str, Depends(oauth2_scheme)], redis: Redis = Depends(get_redis)
):
    username = decode_token(token)
    if is_token_blacklisted(token, redis):
        raise UnauthorizedException("User is logged out")
    return username


def authenticate_user(username: str, password: str, authRepo: UserRepository):
    user = authRepo.getByUsername(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(user: UserCreate, authRepo: UserRepository = Depends()):
    existing_user = authRepo.getByUsername(user.username)
    if existing_user:
        raise ResourceAlreadyExistsException(resource="User", resource_id=user.username)
    user_dict = user.model_dump()
    user_dict["hashed_password"] = get_password_hash(user.password)
    db_user = UserInDB.model_validate(user_dict)
    return authRepo.create(db_user)


def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    authRepo: UserRepository = Depends(),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, authRepo)
    if not user:
        raise InvalidCredentialsException("Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=timedelta(days=7)
    )
    max_age = 7 * 24 * 60 * 60
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=max_age,
        expires=max_age,
        samesite="None",
        secure=True,
    )
    return Token(access_token=access_token, token_type="bearer")


def refresh_token(request: Request) -> Token:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise InvalidTokenException("Refresh token missing")

    username = decode_token(refresh_token)
    if not username:
        raise InvalidTokenException("Invalid refresh token")

    new_access_token = create_access_token(data={"sub": username})
    return Token(access_token=new_access_token, token_type="bearer")


def logout(
    request: Request,
    response: Response,
    access_token=Depends(oauth2_scheme),
    redis: Redis = Depends(get_redis),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise InvalidTokenException("Refresh token missing")
    try:
        blacklist_tokens(access_token, redis)
        response.delete_cookie("refresh_token")
        return {"message": "Logout successful"}
    except InvalidTokenError:
        raise InvalidTokenException("Invalid refresh token")
