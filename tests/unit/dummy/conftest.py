import pytest


@pytest.fixture(scope="session")
def dummy_approved() -> bool:
    return True
