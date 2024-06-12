import sys
from functools import lru_cache
from pathlib import Path


class Settings:
    PLATFORM: str = sys.platform
    BASE_PATH: Path = Path(__file__).resolve().parent

    TOOLS_PATH: Path = BASE_PATH / 'Tools'
    SANDBOX_PATH: Path = TOOLS_PATH / 'SandBox'


@lru_cache
def get_settings():
    return Settings()

