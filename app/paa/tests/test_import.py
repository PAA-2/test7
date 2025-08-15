import pytest
from django.core.management import call_command
from django.contrib.auth import get_user_model

from paa.models import Plan
from paa.models_import import ImportProfile

User = get_user_model()


@pytest.mark.django_db
def test_import_excel(tmp_path):
    user = User.objects.create(username="owner")
    plan = Plan.objects.create(code="P001", name="Plan Test", owner=user)
    ImportProfile.objects.create(
        name="TestProfile", mapping={"A": "code", "B": "title", "C": "description"}
    )

    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "plan d’action"
    for _ in range(10):
        ws.append([])
    ws.append(["A001", "Titre 1", "Desc 1"])
    ws.append(["A002", "Titre 2", "Desc 2"])
    file_path = tmp_path / "test.xlsx"
    wb.save(file_path)

    call_command("import_plan", "P001", str(file_path))

    assert plan.actionplan_set.count() >= 0
