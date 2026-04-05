"""Shared configuration for GAIA PRIME services."""
from functools import lru_cache
from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "GAIA PRIME"
    environment: str = "production"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./gaia_prime.db"
    postgres_url: Optional[str] = None

    # Security
    secret_key: str = "change-me-in-production"
    api_key_header: str = "X-GAIA-API-Key"

    # Service ports
    gaia_prime_port: int = 8000
    phuphadang_port: int = 8001
    chronos_port: int = 8002
    unicorn_port: int = 8003

    # Local-only — never expose to public internet
    host: str = "127.0.0.1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
