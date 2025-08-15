from django.apps import AppConfig


class PaaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "paa"
    verbose_name = "Plans d'Actions"

    def ready(self):  # pragma: no cover - import signals for side effects
        from . import models_attachments  # noqa: F401
        import paa.signals  # noqa: F401
