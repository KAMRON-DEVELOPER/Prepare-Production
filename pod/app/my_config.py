from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    REDIS_URL: str = ""
    
    model_config = SettingsConfigDict(env_file=[".env", Path(__file__).parents[2] / ".env"], env_file_encoding="utf-8", extra="ignore")


def get_secrets():
    database_url = Path("/run/secrets/DATABASE_URL").read_text().strip()
    redis_url = Path("/run/secrets/REDIS_URL").read_text().strip()
    return {
        "DATABASE_URL": database_url,
        "REDIS_URL": redis_url
    }

@lru_cache
def get_settings():
    return Settings()
