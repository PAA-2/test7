import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice


@pytest.mark.django_db
def test_admin_dashboard_access(client, django_user_model):
    sa_group = Group.objects.create(name="SA")
    user_sa = django_user_model.objects.create_user("super")
    user_sa.groups.add(sa_group)
    TOTPDevice.objects.create(user=user_sa, name="default", confirmed=True)

    user = django_user_model.objects.create_user("user")

    client.force_login(user_sa)
    resp = client.get(reverse("admin_dashboard"))
    assert resp.status_code == 200

    client.force_login(user)
    resp = client.get(reverse("admin_dashboard"))
    assert resp.status_code in {302, 403}
