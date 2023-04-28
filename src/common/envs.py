import os
from typing import Optional


def string_env(env: str, default: Optional[str] = None) -> Optional[str]:
    result = os.getenv(env, default=default)
    return result
