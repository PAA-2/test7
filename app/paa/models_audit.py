from django.db import models


class AuditLog(models.Model):
    ts = models.DateTimeField(auto_now_add=True)
    actor = models.CharField(max_length=150, blank=True)
    verb = models.CharField(max_length=50)
    obj_type = models.CharField(max_length=100)
    obj_id = models.CharField(max_length=64)
    before = models.JSONField(null=True, blank=True)
    after = models.JSONField(null=True, blank=True)
    ip = models.CharField(max_length=45, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-ts"]

    def save(self, *args, **kwargs):
        if self.pk:
            return
        super().save(*args, **kwargs)
