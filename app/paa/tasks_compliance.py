from celery import shared_task
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
import tempfile
import csv
from .retention import purge_due


@shared_task
def purge_due_task():
    return purge_due()


User = get_user_model()


@shared_task
def monthly_permissions_report():
    sa_emails = list(
        User.objects.filter(groups__name="SA")
        .exclude(email="")
        .values_list("email", flat=True)
        .distinct()
    )
    if not sa_emails:
        return 0
    with tempfile.NamedTemporaryFile(
        "w+", newline="", encoding="utf-8", suffix=".csv", delete=False
    ) as f:
        w = csv.writer(f)
        w.writerow(["username", "roles"])
        for u in User.objects.all().prefetch_related("groups"):
            w.writerow([u.username, ";".join(u.groups.values_list("name", flat=True))])
        f.flush()
        mail = EmailMessage(
            "[PAA] Rapport mensuel des permissions",
            "Ci-joint le rapport des rôles.",
            to=sa_emails,
        )
        mail.attach_file(f.name)
        mail.send(fail_silently=True)
    return 1
