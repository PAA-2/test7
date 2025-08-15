from django.apps import AppConfig


class AssistantliteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "assistantlite"

    def ready(self):  # pragma: no cover
        from . import rules  # noqa: F401
