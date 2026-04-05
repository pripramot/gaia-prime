"""GAIA PRIME service settings."""
from functools import lru_cache

from gaia_shared.config import Settings


class GaiaPrimeSettings(Settings):
    app_name: str = "GAIA PRIME"
    service_id: str = "gaia-prime"


@lru_cache
def get_app_settings() -> GaiaPrimeSettings:
    return GaiaPrimeSettings()
