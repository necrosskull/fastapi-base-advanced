from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_url: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


settings: Settings = get_settings()


@lru_cache
def get_db_url(engine: str) -> str:
    return f"postgresql+{engine}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"


@lru_cache
def get_test_db_url(engine: str) -> str:
    return f"postgresql+{engine}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}_test"
