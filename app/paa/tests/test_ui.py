import csv
import io
from datetime import date, timedelta

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse

from django.core.cache import cache
from paa.models import Action
from paa.cache_utils import KPI_CACHE_KEY


@pytest.mark.django_db
def test_dashboard_kpis(client, django_user_model):
    user = django_user_model.objects.create_user("u")
    client.force_login(user)
    cache.delete(KPI_CACHE_KEY)
    Action.objects.create(title="a1", created_by=user, status="EN_COURS")
    Action.objects.create(
        title="a2", created_by=user, due_date=date.today() - timedelta(days=1)
    )
    Action.objects.create(title="a3", created_by=user, status="EN_TRAITEMENT")
    Action.objects.create(
        title="a4",
        created_by=user,
        status="CLOTUREE",
    )
    resp = client.get(reverse("dashboard"))
    assert resp.status_code == 200
    kpis = resp.context["kpis"]
    assert kpis["total"] == 4
    assert kpis["en_cours"] == 1
    assert kpis["en_traitement"] == 1
    assert kpis["retards"] == 1
    assert kpis["cloturees_7j"] == 1


@pytest.mark.django_db
def test_actions_list_filter(client, django_user_model):
    cache.clear()
    user = django_user_model.objects.create_user("u")
    client.force_login(user)
    Action.objects.create(title="foo", created_by=user)
    Action.objects.create(title="bar", created_by=user)
    resp = client.get(reverse("actions_list"), {"q": "foo"})
    assert resp.status_code == 200
    content = resp.content.decode()
    assert "foo" in content
    assert "bar" not in content


@pytest.mark.django_db
def test_action_detail_permissions(client, django_user_model):
    sa_group = Group.objects.create(name="SA")
    sa_user = django_user_model.objects.create_user("sa")
    sa_user.groups.add(sa_group)
    action = Action.objects.create(title="a", created_by=sa_user)

    client.force_login(sa_user)
    resp = client.get(reverse("action_detail", args=[action.id]))
    assert resp.status_code == 200

    user = django_user_model.objects.create_user("u")
    client.force_login(user)
    resp = client.get(reverse("action_detail", args=[action.id]))
    assert resp.status_code == 302


@pytest.mark.django_db
def test_kanban_view(client, django_user_model):
    user = django_user_model.objects.create_user("u")
    client.force_login(user)
    resp = client.get(reverse("kanban"))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_export_actions_csv(client, django_user_model):
    user = django_user_model.objects.create_user("u")
    client.force_login(user)
    Action.objects.create(title="a1", created_by=user)
    resp = client.get(reverse("export_actions_csv"))
    assert resp.status_code == 200
    reader = csv.reader(io.StringIO(resp.content.decode()))
    rows = list(reader)
    assert rows[0] == ["Code", "Titre", "Statut", "Priorité", "Échéance", "J"]
    assert len(rows) == 2
