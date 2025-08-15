from pathlib import Path
from .base import *  # noqa: F401,F403

DEBUG = True
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.sqlite3",
    }
}
