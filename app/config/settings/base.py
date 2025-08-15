import environ
from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY", default="change-me")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "paa",
    "assistantlite",
]

INSTALLED_APPS += [
    "guardian",
    "django.contrib.postgres",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "axes",
]

MIDDLEWARE = [
    "axes.middleware.AxesMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "paa.security.SecurityHeadersMiddleware",
    "paa.security.AdminIPAllowlistMiddleware",
    "paa.security.CurrentUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "paa.auth_gate.enforce_mfa_middleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="paa"),
        "USER": env("POSTGRES_USER", default="paa"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="paa"),
        "HOST": env("POSTGRES_HOST", default="db"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_CACHE_URL", default="redis://redis:6379/2"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "paa",
        "TIMEOUT": 300,
    }
}

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Algiers"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

FERNET_KEY = env(
    "FERNET_KEY",
    default="MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA=",
)

AUTHENTICATION_BACKENDS = (
    "paa.sso_backend.PlaceholderSSOBackend",
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

ANONYMOUS_USER_NAME = "anonymous"

AXES_FAILURE_LIMIT = int(env("AXES_FAILURE_LIMIT", default=5))
AXES_COOLOFF_TIME = int(env("AXES_COOLOFF_TIME", default=30))
AXES_LOCKOUT_PARAMETERS = ["username", "ip_address"]

MFA_REQUIRED_ROLES = ["SA", "PP"]

SSO_ENABLED = env.bool("SSO_ENABLED", default=False)

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@paa.local")
EXPORT_DIR = env("EXPORT_DIR", default="/media/exports")

RETENTION_DAYS = int(env("RETENTION_DAYS", default=365))
PURGE_GRACE_DAYS = int(env("PURGE_GRACE_DAYS", default=30))

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://redis:6379/1")
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

CELERY_BEAT_SCHEDULE = {
    "send-reminders-daily": {
        "task": "paa.tasks.send_reminders",
        "schedule": timedelta(days=1),
        "options": {"queue": "default"},
    },
    "check-stale-en-traitement": {
        "task": "paa.tasks.check_stale_en_traitement",
        "schedule": timedelta(hours=6),
    },
    "send-weekly-digest": {
        "task": "paa.tasks.send_weekly_digest",
        "schedule": timedelta(days=1),
    },
    "run-scheduled-syncs": {
        "task": "paa.tasks.run_scheduled_syncs",
        "schedule": timedelta(days=1),
    },
    "recalc-consolidated": {
        "task": "paa.tasks.recalc_consolidated",
        "schedule": timedelta(days=1),
    },
}

CELERY_BEAT_SCHEDULE.update(
    {
        "refresh-mv-nightly": {
            "task": "paa.tasks_perf.refresh_consolidated_mv",
            "schedule": timedelta(days=1),
        },
        "warm-kpi-cache-5min": {
            "task": "paa.tasks_perf.warm_kpi_cache",
            "schedule": timedelta(minutes=5),
        },
        "purge-due-daily": {
            "task": "paa.tasks_compliance.purge_due_task",
            "schedule": timedelta(days=1),
        },
        "permissions-report-monthly": {
            "task": "paa.tasks_compliance.monthly_permissions_report",
            "schedule": 60 * 60 * 24 * 30,
        },
    }
)

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SAMESITE = "Strict"

SECURE_REFERRER_POLICY = "strict-origin"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
