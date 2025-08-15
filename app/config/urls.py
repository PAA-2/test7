from django.urls import path, include
from django.http import JsonResponse, HttpResponse
from django.contrib import admin
from paa import views_mfa, views_compliance


def health(request):
    return JsonResponse({"status": "ok", "version": "1.0.0"})


urlpatterns = [
    path("", health),
    path("", include("paa.urls_search")),
    path("paa/adminpanel/", include("paa.urls_adminpanel")),
    path("", include("paa.urls_ui")),
    path("assistant/", include("assistantlite.urls")),
    path("admin/", admin.site.urls),
]

try:  # pragma: no cover - optional MFA routes
    import django_otp.urls as otp_urls

    urlpatterns += [path("otp/", include(otp_urls))]
except ModuleNotFoundError:  # pragma: no cover
    pass

urlpatterns += [
    path("mfa/setup/", views_mfa.mfa_setup, name="mfa_setup"),
    path("mfa/verify/", views_mfa.mfa_verify, name="mfa_verify"),
    path(
        "compliance/export/<int:user_id>/",
        views_compliance.export_user_data,
        name="export_user_data",
    ),
    path(
        "security.txt",
        lambda r: HttpResponse(
            "Contact: security@paa.local\n", content_type="text/plain"
        ),
    ),
    path(
        "robots.txt",
        lambda r: HttpResponse(
            "User-agent: *\nDisallow: /",
            content_type="text/plain",
        ),
    ),
]
