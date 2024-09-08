import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftest() -> None:
    print("LOL")
