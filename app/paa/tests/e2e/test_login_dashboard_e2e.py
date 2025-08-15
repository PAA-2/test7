import pytest
from django.contrib.auth.models import User, Group

pytestmark = pytest.mark.e2e


@pytest.mark.django_db
def test_login_and_dashboard(live_server, page):
    # Seed SA
    g, _ = Group.objects.get_or_create(name="SA")
    u, _ = User.objects.get_or_create(username="user_SA")
    u.set_password("test1234")
    u.is_staff = True
    u.save()
    u.groups.add(g)

    # Login
    page.goto(f"{live_server.url}/admin/login/?next=/dashboard/")
    page.fill('input[name="username"]', "user_SA")
    page.fill('input[name="password"]', "test1234")
    page.click('input[type="submit"]')

    # Accès dashboard
    page.goto(f"{live_server.url}/dashboard/")
    page.wait_for_selector("text=Dashboard")
    assert "Dashboard" in page.content()
