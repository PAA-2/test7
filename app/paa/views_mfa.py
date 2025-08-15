import io
import base64
import qrcode
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django_otp.plugins.otp_totp.models import TOTPDevice


def _role_names(user):
    return list(user.groups.values_list("name", flat=True))


@login_required
def mfa_setup(request):
    if not any(r in settings.MFA_REQUIRED_ROLES for r in _role_names(request.user)):
        messages.info(request, "MFA non requise pour votre rôle.")
        return redirect("dashboard")

    device, _ = TOTPDevice.objects.get_or_create(
        user=request.user, name="default", confirmed=False
    )
    otpauth = device.config_url
    img = qrcode.make(otpauth)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    if request.method == "POST":
        token = request.POST.get("token", "").strip()
        if device.verify_token(token):
            device.confirmed = True
            device.save(update_fields=["confirmed"])
            messages.success(request, "MFA TOTP activée.")
            return redirect("dashboard")
        messages.error(request, "Code MFA invalide.")

    return render(request, "paa/mfa_setup.html", {"qr_b64": qr_b64})


@login_required
def mfa_verify(request):
    if request.method == "POST":
        token = request.POST.get("token", "").strip()
        dev = TOTPDevice.objects.filter(
            user=request.user, name="default", confirmed=True
        ).first()
        if dev and dev.verify_token(token):
            messages.success(request, "MFA vérifiée.")
            return redirect("dashboard")
        messages.error(request, "Code MFA invalide.")
    return render(request, "paa/mfa_verify.html")
