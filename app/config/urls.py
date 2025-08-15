from django.urls import path, include
from django.http import JsonResponse


def health(request):
    return JsonResponse({"status": "ok", "version": "1.0.0"})


urlpatterns = [
    path("", health),
    path("", include("paa.urls_search")),
    path("adminpanel/", include("paa.urls_adminpanel")),
    path("", include("paa.urls_ui")),
]
