import os
import pytest


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")


@pytest.fixture(scope="session")
def browser_type_launch_args():
    # Empêche le sandboxing (utile en CI conteneur)
    return {"args": ["--no-sandbox"]}
