import pytest
from django.contrib.auth import get_user_model
from paa.models import Plan, Action, ActionPlan


User = get_user_model()


@pytest.mark.django_db
def test_create_plan_and_action():
    user = User.objects.create(username="testuser")
    plan = Plan.objects.create(code="P001", name="Plan Test", owner=user)
    action = Action.objects.create(code="A001", title="Action Test", created_by=user)
    ActionPlan.objects.create(action=action, plan=plan)
    assert plan.code == "P001"
    assert action.code == "A001"
    assert ActionPlan.objects.count() == 1
