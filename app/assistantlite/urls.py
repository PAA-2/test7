from django.urls import path
from . import views


urlpatterns = [
    path("trigger/", views.trigger, name="assistant_trigger"),
    path("faq/", views.faq_list, name="assistant_faq"),
    path("logs/", views.logs, name="assistant_logs"),
]
