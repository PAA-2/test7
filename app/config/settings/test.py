from pathlib import Path
from .base import *  # noqa: F401,F403

DEBUG = True
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "paa_test.sqlite3",
    }
}
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
