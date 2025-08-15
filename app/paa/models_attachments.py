import os
from django.db import models
from django.contrib.postgres.indexes import GinIndex


def attachment_upload_to(instance, filename):
    return os.path.join("attachments", instance.action.code, filename)


class Attachment(models.Model):
    action = models.ForeignKey(
        "paa.Action", on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to=attachment_upload_to)
    mime = models.CharField(max_length=100, blank=True)
    size = models.PositiveIntegerField(default=0)
    sha256 = models.CharField(max_length=64, blank=True)
    version = models.PositiveIntegerField(default=1)
    ocr_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            GinIndex(
                fields=["ocr_text"],
                name="idx_attachment_ocr_gin",
                opclasses=["gin_trgm_ops"],
            ),
        ]
