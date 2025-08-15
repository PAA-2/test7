from django.urls import path, include
from django.http import JsonResponse
from django.contrib import admin


def health(request):
    return JsonResponse({"status": "ok", "version": "1.0.0"})


urlpatterns = [
    path("", health),
    path("", include("paa.urls_search")),
    path("paa/adminpanel/", include("paa.urls_adminpanel")),
    path("", include("paa.urls_ui")),
    path("admin/", admin.site.urls),
]

try:  # pragma: no cover - optional MFA routes
    import django_otp.urls as otp_urls

    urlpatterns += [path("otp/", include(otp_urls))]
except ModuleNotFoundError:  # pragma: no cover
    pass
