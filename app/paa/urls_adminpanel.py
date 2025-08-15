from django.urls import path
from . import views_adminpanel

urlpatterns = [
    path("", views_adminpanel.admin_dashboard, name="admin_dashboard"),
    path("branding/", views_adminpanel.branding_view, name="branding"),
    path("features/", views_adminpanel.feature_flags_view, name="feature_flags"),
    path("smtp-test/", views_adminpanel.smtp_test_view, name="smtp_test"),
    path(
        "import-profiles/",
        views_adminpanel.import_profiles_view,
        name="import_profiles",
    ),
    path("sync-reports/", views_adminpanel.sync_report_view, name="sync_reports"),
]
