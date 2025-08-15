import pytest
from django.contrib.auth.models import Group, User


@pytest.mark.django_db
def test_trigger_create_action(client):
    g, _ = Group.objects.get_or_create(name="P")
    u = User.objects.create_user(username="pilot", password="x")
    u.groups.add(g)
    client.login(username="pilot", password="x")
    resp = client.post("/assistant/trigger/", {"q": "nouvelle action: Test palette"})
    assert resp.status_code == 200
    assert resp.json().get("ok") is True
