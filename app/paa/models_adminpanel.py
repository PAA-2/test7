from django.db import models
from paa.crypto import EncryptedTextField


class SystemSettings(models.Model):
    branding = models.JSONField(default=dict)
    colors = models.JSONField(default=dict)
    feature_flags = models.JSONField(default=dict)
    smtp_tested = models.BooleanField(default=False)
    admin_ip_allowlist = models.JSONField(default=list)
    smtp_password = EncryptedTextField(blank=True)

    def __str__(self) -> str:
        return "Paramètres système"
