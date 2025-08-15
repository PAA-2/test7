import pytest
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from paa.models import Plan, Action
from paa.helpers import can_edit

User = get_user_model()


@pytest.mark.django_db
def test_user_cannot_edit_without_role():
    u = User.objects.create_user(username="user", password="test1234")
    p = User.objects.create_user(username="pilot", password="test1234")
    g, _ = Group.objects.get_or_create(name="P")
    p.groups.add(g)
    Plan.objects.create(code="P001", name="Plan", owner=p)
    a = Action.objects.create(code="A001", title="A", created_by=p)
    # L'utilisateur lambda ne peut pas éditer
    assert not can_edit(a, u)
