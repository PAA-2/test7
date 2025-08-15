import base64
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from paa.models import Action
from paa.models_adminpanel import SystemSettings
from paa.models_audit import AuditLog


@pytest.mark.django_db
def test_encrypted_field_roundtrip():
    settings.FERNET_KEY = base64.urlsafe_b64encode(b"0" * 32).decode()
    obj = SystemSettings.objects.create(smtp_password="secret")
    obj.refresh_from_db()
    assert obj.smtp_password == "secret"


@pytest.mark.django_db
def test_audit_log_created():
    User = get_user_model()
    u = User.objects.create(username="u")
    a = Action.objects.create(code="A100", title="T", created_by=u)
    assert AuditLog.objects.filter(
        obj_type="Action", obj_id=str(a.pk), verb="created"
    ).exists()
    a.title = "T2"
    a.save()
    assert AuditLog.objects.filter(
        obj_type="Action", obj_id=str(a.pk), verb="updated"
    ).exists()
