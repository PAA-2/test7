from datetime import date, timedelta
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from celery import shared_task
from .models import Action
from .models_import import ImportProfile, SyncSchedule
from .importer import import_plan_from_excel

User = get_user_model()

REMINDER_OFFSETS = (-7, -3, -1, 0)
STALE_EN_TRAITEMENT_DAYS = 7


def _action_is_due_for_offset(action, offset_days):
    if action.status == "CLOTUREE" or not action.due_date:
        return False
    j = (action.due_date - date.today()).days
    if offset_days == 0:
        return j <= 0
    return j == abs(offset_days)


def _send_action_email(subject, message, users):
    recipients = [u.email for u in users if u.email]
    if not recipients:
        return 0
    return send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True
    )


@shared_task
def send_reminders():
    qs = Action.objects.exclude(status__in=["CLOTUREE", "ARCHIVEE"]).filter(
        due_date__isnull=False
    )
    sent = 0
    for action in qs:
        if any(_action_is_due_for_offset(action, o) for o in REMINDER_OFFSETS):
            users = list(action.responsables.all())
            if users:
                subject = f"[PAA] Rappel — {action.code} {action.title}"
                j = (action.due_date - date.today()).days
                message = (
                    f"Action: {action.code} — {action.title}\n"
                    f"Échéance: {action.due_date} (J={j})\n"
                    f"Statut: {action.status}"
                )
                sent += _send_action_email(subject, message, users)
    return sent


@shared_task
def check_stale_en_traitement():
    threshold_date = date.today() - timedelta(days=STALE_EN_TRAITEMENT_DAYS)
    stale = Action.objects.filter(
        status="EN_TRAITEMENT", updated_at__date__lte=threshold_date
    )
    if not stale.exists():
        return 0
    pp_users = User.objects.filter(groups__name="PP")
    lines = [
        f"{a.code} — {a.title} (dernière maj: {a.updated_at.date()})" for a in stale
    ]
    subject = "[PAA] Actions EN_TRAITEMENT stagnantes"
    message = (
        "Les actions suivantes sont en EN_TRAITEMENT depuis trop longtemps:\n"
        + "\n".join(lines)
    )
    return _send_action_email(subject, message, pp_users)


@shared_task
def send_weekly_digest():
    if date.today().weekday() != 0:
        return 0
    sa_pp_p = User.objects.filter(
        Q(groups__name="SA") | Q(groups__name="PP") | Q(groups__name="P")
    ).distinct()
    kpis = {
        "total": Action.objects.count(),
        "en_cours": Action.objects.filter(status="EN_COURS").count(),
        "en_traitement": Action.objects.filter(status="EN_TRAITEMENT").count(),
        "retards": Action.objects.filter(
            due_date__isnull=False,
            status__in=["A_FAIRE", "EN_COURS", "EN_TRAITEMENT"],
            due_date__lt=date.today(),
        ).count(),
        "cloturees_7j": Action.objects.filter(
            status="CLOTUREE", updated_at__date__gte=(date.today() - timedelta(days=7))
        ).count(),
    }
    subject = "[PAA] Digest hebdo"
    message = (
        "Résumé 7j:\n"
        f"- Total actions: {kpis['total']}\n"
        f"- En cours: {kpis['en_cours']}\n"
        f"- En traitement: {kpis['en_traitement']}\n"
        f"- En retard: {kpis['retards']}\n"
        f"- Clôturées (7j): {kpis['cloturees_7j']}\n"
    )
    return _send_action_email(subject, message, sa_pp_p)


@shared_task
def run_scheduled_syncs():
    schedules = SyncSchedule.objects.filter(enabled=True, plan__mode="EXCEL")
    count = 0
    for s in schedules:
        profile = ImportProfile.objects.first()
        if not profile:
            continue
        file_path = f"/media/{s.plan.code}.xlsx"
        try:
            import_plan_from_excel(s.plan, file_path, profile)
            count += 1
        except Exception:
            continue
    return count


@shared_task
def recalc_consolidated():
    return Action.objects.count()
