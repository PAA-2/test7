import pytest
from django.contrib.auth.models import Group

from paa.helpers import (
    ROLE_PILOTE,
    ROLE_PILOTE_PROCESSUS,
    ROLE_SUPER_ADMIN,
    ROLE_UTILISATEUR,
    can_edit,
    can_transition,
    can_view,
)
from paa.models import Action, Plan


@pytest.fixture
def setup_users(django_user_model):
    users = {}
    for role in [
        ROLE_SUPER_ADMIN,
        ROLE_PILOTE_PROCESSUS,
        ROLE_PILOTE,
        ROLE_UTILISATEUR,
    ]:
        user = django_user_model.objects.create(username=f"user_{role}")
        group = Group.objects.create(name=role)
        user.groups.add(group)
        users[role] = user
    return users


@pytest.mark.django_db
def test_permissions_by_role(setup_users):
    plan = Plan.objects.create(
        code="P001", name="Plan Test", owner=setup_users[ROLE_PILOTE]
    )
    action = Action.objects.create(
        code="A001", title="Action Test", created_by=setup_users[ROLE_PILOTE]
    )
    action.plan = plan

    assert can_view(plan, setup_users[ROLE_SUPER_ADMIN])
    assert can_view(plan, setup_users[ROLE_PILOTE_PROCESSUS])
    assert can_view(plan, setup_users[ROLE_PILOTE])
    assert not can_view(plan, setup_users[ROLE_UTILISATEUR])

    assert can_edit(plan, setup_users[ROLE_SUPER_ADMIN])
    assert can_edit(plan, setup_users[ROLE_PILOTE_PROCESSUS])
    assert can_edit(plan, setup_users[ROLE_PILOTE])
    assert not can_edit(plan, setup_users[ROLE_UTILISATEUR])

    assert can_transition(action, setup_users[ROLE_SUPER_ADMIN])
    assert can_transition(action, setup_users[ROLE_PILOTE_PROCESSUS])
    assert can_transition(action, setup_users[ROLE_PILOTE])
    assert not can_transition(action, setup_users[ROLE_UTILISATEUR])
