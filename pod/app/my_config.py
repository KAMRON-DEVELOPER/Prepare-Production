from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = ""
    REDIS_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore") # secrets_dir="/run/secrets"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"Loaded DB_URL: {self.DB_URL}")
        print(f"Loaded REDIS_URL: {self.REDIS_URL}")
        print(f"Current working directory: {Path.cwd()}")
        print(f"Trying env files: {self.model_config['env_file']}")


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
