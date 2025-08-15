import pytest
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from paa.models import Action, Plan

User = get_user_model()


@pytest.mark.django_db
def test_search_basic(client):
    u = User.objects.create_user(username="u", password="pw")
    g = Group.objects.create(name="U")
    u.groups.add(g)
    client.login(username="u", password="pw")

    p = User.objects.create_user(username="pilot", password="pw")
    Plan.objects.create(code="P001", name="Plan", owner=p)
    a = Action.objects.create(
        code="A001",
        title="Pompe Hydraulique",
        description="Maintenance périodique",
        created_by=p,
    )
    a.responsables.add(u)

    resp = client.get("/search/?q=hydraulique")
    assert resp.status_code == 200
