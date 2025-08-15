from django.db import models
from django.utils import timezone


class AssistantLog(models.Model):
    ts = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    intent = models.CharField(max_length=120)
    payload = models.JSONField(default=dict)
    result = models.JSONField(default=dict)

    class Meta:
        ordering = ["-ts"]


class FAQ(models.Model):
    question = models.CharField(max_length=300, unique=True)
    answer_md = models.TextField()

    def __str__(self):
        return self.question[:60]
