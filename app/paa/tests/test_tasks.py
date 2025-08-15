import pytest
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from paa.models import Action, Plan

User = get_user_model()


@pytest.mark.django_db
def test_send_reminders_basic(celery_app, settings):
    settings.DEFAULT_FROM_EMAIL = "no-reply@example.com"
    u = User.objects.create(username="u", email="u@example.com")
    Plan.objects.create(code="P001", name="Plan", owner=u)
    action = Action.objects.create(
        code="A001", title="T", created_by=u, due_date=date.today() + timedelta(days=7)
    )
    action.responsables.add(u)
    from paa.tasks import send_reminders

    sent = send_reminders()
    assert isinstance(sent, int)
