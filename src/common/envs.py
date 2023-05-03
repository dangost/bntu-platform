import os
from typing import Optional


def string_env(env: str, default: Optional[str] = None) -> Optional[str]:
    result = os.getenv(env, default=default)
    return result if result is not None else None


def int_env(env: str, default: Optional[int] = None) -> Optional[int]:
    result = os.getenv(env, default=default)
    return int(result) if result is not None else None
