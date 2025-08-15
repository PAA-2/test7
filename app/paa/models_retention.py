from django.db import models
from django.utils import timezone
from datetime import timedelta


class RetentionMark(models.Model):
    """Marque un objet pour suppression différée (grâce légale)."""

    model = models.CharField(max_length=100)
    object_id = models.CharField(max_length=64)
    reason = models.CharField(max_length=255, blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)

    def is_due(self, grace_days: int) -> bool:
        return self.marked_at + timedelta(days=grace_days) <= timezone.now()
