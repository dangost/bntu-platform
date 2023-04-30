import pytest

"""
This is example of pytest fixtures
"""


@pytest.fixture(scope="session")
def jwt_secret() -> str:
    return "secret"
