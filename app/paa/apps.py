from django.apps import AppConfig


class PaaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "paa"
    verbose_name = "Plans d'Actions"

    def ready(self):  # pragma: no cover - import signals for side effects
        import paa.signals  # noqa: F401
