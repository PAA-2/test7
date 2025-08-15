from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required, user_passes_test

from paa.models_adminpanel import SystemSettings
from paa.forms_adminpanel import (
    BrandingForm,
    FeatureFlagsForm,
    SMTPTestForm,
    ImportProfileForm,
)
from paa.models_import import ImportProfile, SyncReport


def is_super_admin(user):
    return user.groups.filter(name="SA").exists()


@login_required
@user_passes_test(is_super_admin)
def admin_dashboard(request):
    settings_obj, _ = SystemSettings.objects.get_or_create(pk=1)
    return render(request, "paa/adminpanel/dashboard.html", {"settings": settings_obj})


@login_required
@user_passes_test(is_super_admin)
def branding_view(request):
    settings_obj, _ = SystemSettings.objects.get_or_create(pk=1)
    if request.method == "POST":
        form = BrandingForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Branding mis à jour.")
            return redirect("admin_dashboard")
    else:
        form = BrandingForm(instance=settings_obj)
    return render(request, "paa/adminpanel/branding.html", {"form": form})


@login_required
@user_passes_test(is_super_admin)
def feature_flags_view(request):
    settings_obj, _ = SystemSettings.objects.get_or_create(pk=1)
    if request.method == "POST":
        form = FeatureFlagsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Feature flags mis à jour.")
            return redirect("admin_dashboard")
    else:
        form = FeatureFlagsForm(instance=settings_obj)
    return render(request, "paa/adminpanel/feature_flags.html", {"form": form})


@login_required
@user_passes_test(is_super_admin)
def smtp_test_view(request):
    if request.method == "POST":
        form = SMTPTestForm(request.POST)
        if form.is_valid():
            try:
                send_mail(
                    "Test SMTP",
                    "Ceci est un test.",
                    "no-reply@example.com",
                    [form.cleaned_data["email"]],
                )
                messages.success(request, "E-mail de test envoyé avec succès.")
            except BadHeaderError:
                messages.error(request, "Erreur d'envoi SMTP.")
            return redirect("admin_dashboard")
    else:
        form = SMTPTestForm()
    return render(request, "paa/adminpanel/smtp_test.html", {"form": form})


@login_required
@user_passes_test(is_super_admin)
def import_profiles_view(request):
    profiles = ImportProfile.objects.all()
    if request.method == "POST":
        form = ImportProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil import créé/mis à jour.")
            return redirect("import_profiles")
    else:
        form = ImportProfileForm()
    return render(
        request,
        "paa/adminpanel/import_profiles.html",
        {"profiles": profiles, "form": form},
    )


@login_required
@user_passes_test(is_super_admin)
def sync_report_view(request):
    reports = SyncReport.objects.all().order_by("-ts")[:50]
    return render(
        request,
        "paa/adminpanel/sync_reports.html",
        {"reports": reports},
    )
