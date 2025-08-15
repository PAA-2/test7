import pytest
from django.contrib.auth.models import User, Group
from paa.models import Plan, Action

pytestmark = pytest.mark.e2e


@pytest.mark.django_db
def test_list_actions_and_open_detail(live_server, page):
    g, _ = Group.objects.get_or_create(name="P")
    p, _ = User.objects.get_or_create(username="pilot")
    p.set_password("test1234")
    p.is_staff = True
    p.save()
    p.groups.add(g)
    Plan.objects.create(code="P001", name="Plan", owner=p)
    a = Action.objects.create(code="A001", title="Action E2E", created_by=p)

    # Login
    page.goto(f"{live_server.url}/admin/login/?next=/actions/")
    page.fill('input[name="username"]', "pilot")
    page.fill('input[name="password"]', "test1234")
    page.click('input[type="submit"]')

    # Liste
    page.goto(f"{live_server.url}/actions/")
    page.wait_for_selector("text=Liste Actions")
    page.click(f"a[href='/actions/{a.id}/']")

    # Détail
    page.wait_for_selector(f"text={a.title}")
    assert a.title in page.content()
