from django.db import models


class ImportProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sheet_name = models.CharField(max_length=100, default="plan d’action")
    header_row = models.PositiveIntegerField(default=11)
    mapping = models.JSONField(default=dict)
    allow_user_creation = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SyncReport(models.Model):
    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)
    ts = models.DateTimeField(auto_now_add=True)
    created_count = models.PositiveIntegerField(default=0)
    updated_count = models.PositiveIntegerField(default=0)
    skipped_count = models.PositiveIntegerField(default=0)
    errors = models.JSONField(default=list)

    def __str__(self):
        return f"Rapport {self.plan.code} — {self.ts}"
