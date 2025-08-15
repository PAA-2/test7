import pytest
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from paa.models import Action
from paa.services import compute_j_delta, request_check, accept_check

User = get_user_model()


@pytest.mark.django_db
def test_compute_j_delta_non_cloturee():
    user = User.objects.create(username="t1")
    action = Action.objects.create(
        title="Test J", created_by=user, due_date=date.today() + timedelta(days=5)
    )
    delta = compute_j_delta(action)
    assert delta == 5


@pytest.mark.django_db
def test_request_and_accept_check():
    user = User.objects.create(username="t2")
    sa_group = Group.objects.create(name="SA")
    user.groups.add(sa_group)
    action = Action.objects.create(title="Test PDCA", created_by=user)
    request_check(action, user)
    assert action.status == "EN_TRAITEMENT"
    accept_check(action, user, "OK")
    assert action.status == "CLOTUREE"
    assert action.efficacy_note == "OK"
