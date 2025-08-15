import pytest
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice


User = get_user_model()


@pytest.mark.django_db
def test_export_user_data(client):
    g, _ = Group.objects.get_or_create(name="SA")
    u = User.objects.create_user(username="sa", password="x", email="sa@local")
    u.groups.add(g)
    TOTPDevice.objects.create(user=u, name="default", confirmed=True)
    client.login(username="sa", password="x")
    resp = client.get(reverse("export_user_data", args=[u.id]))
    assert resp.status_code == 200
    assert resp["Content-Type"].startswith("application/zip")
