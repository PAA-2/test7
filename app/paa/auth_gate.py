from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice


def enforce_mfa_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            role_names = list(request.user.groups.values_list("name", flat=True))
            if any(r in settings.MFA_REQUIRED_ROLES for r in role_names):
                dev_exists = TOTPDevice.objects.filter(
                    user=request.user, name="default", confirmed=True
                ).exists()
                if not dev_exists and request.path not in (
                    "/mfa/setup/",
                    "/mfa/verify/",
                ):
                    messages.warning(
                        request, "MFA requise pour votre rôle. Merci d’activer TOTP."
                    )
                    return redirect("mfa_setup")
        return get_response(request)

    return middleware
