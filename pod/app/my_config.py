import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

if not os.path.exists('/run/secrets'):
    os.makedirs(name="/run/secrets", exist_ok=True)


class Settings(BaseSettings):
    DB_URL: str = ""
    REDIS_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", secrets_dir=("/run/secrets",))


# def get_secrets():
#     database_url = Path("/run/secrets/DB_URL").read_text().strip()
#     redis_url = Path("/run/secrets/REDIS_URL").read_text().strip()
#     return {
#         "DATABASE_URL": database_url,
#         "REDIS_URL": redis_url
#     }


@lru_cache
def get_settings():
    return Settings()
