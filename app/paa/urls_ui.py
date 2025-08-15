from django.urls import path
from . import views_ui

urlpatterns = [
    path("dashboard/", views_ui.dashboard, name="dashboard"),
    path("actions/", views_ui.actions_list, name="actions_list"),
    path("actions/<uuid:pk>/", views_ui.action_detail, name="action_detail"),
    path("kanban/", views_ui.kanban_view, name="kanban"),
    path("export/actions/", views_ui.export_actions_csv, name="export_actions_csv"),
]
