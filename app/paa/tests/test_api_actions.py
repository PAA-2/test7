import pytest
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from paa.models import Plan, Action

User = get_user_model()


@pytest.mark.django_db
def test_create_action_minimal(client):
    # Setup user P
    g, _ = Group.objects.get_or_create(name="P")
    puser = User.objects.create_user(username="pilot", password="test1234")
    puser.groups.add(g)
    client.login(username="pilot", password="test1234")
    owner = puser
    Plan.objects.create(code="P001", name="Plan", owner=owner)

    a = Action.objects.create(code="A001", title="Action API", created_by=owner)
    assert a.code == "A001"
    assert a.title == "Action API"
