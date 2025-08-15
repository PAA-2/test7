from django.conf import settings
from django.apps import apps
from .models_retention import RetentionMark


def mark_for_retention(model_name: str, object_id: str, reason: str = ""):
    RetentionMark.objects.get_or_create(
        model=model_name, object_id=str(object_id), defaults={"reason": reason}
    )


def purge_due():
    due = [
        m for m in RetentionMark.objects.all() if m.is_due(settings.PURGE_GRACE_DAYS)
    ]
    for mark in due:
        model = apps.get_model("paa", mark.model)
        if model:
            try:
                obj = model.objects.get(pk=mark.object_id)
                obj.delete()
            except model.DoesNotExist:
                pass
        mark.delete()
    return len(due)
