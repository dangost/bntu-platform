import hashlib
from typing import Union


def sha256(value: Union[str, bytes]) -> str:
    if isinstance(value, bytes):
        return hashlib.sha256(value).hexdigest()
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
