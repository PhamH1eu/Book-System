from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings:
    DATABASE_DIALECT: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str

class RedisSettings:
    REDIS_HOSTNAME: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str

class DebugSettings:
    DEBUG_MODE: bool

class SecuritySettings:
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

class EnvironmentSettings(BaseSettings, DatabaseSettings, RedisSettings, DebugSettings, SecuritySettings):
    model_config = SettingsConfigDict(env_file=".env")
    pass

@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
