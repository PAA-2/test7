from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from paa.models import Plan, Action
import csv
import sys


User = get_user_model()


class Command(BaseCommand):
    help = "Génère un rapport CSV des permissions/rôles."

    def add_arguments(self, parser):
        parser.add_argument(
            "--out", type=str, default="-", help="Fichier CSV de sortie (défaut stdout)"
        )

    def handle(self, *args, **opts):
        users = User.objects.all().prefetch_related("groups")
        rows = [
            [
                "username",
                "roles",
                "plans_possedes",
                "actions_creees",
                "actions_responsable",
            ]
        ]
        for u in users:
            roles = ";".join(u.groups.values_list("name", flat=True))
            rows.append(
                [
                    u.username,
                    roles,
                    Plan.objects.filter(owner=u).count(),
                    Action.objects.filter(created_by=u).count(),
                    Action.objects.filter(responsables=u).count(),
                ]
            )
        out = (
            sys.stdout
            if opts["out"] == "-"
            else open(opts["out"], "w", newline="", encoding="utf-8")
        )
        w = csv.writer(out)
        w.writerows(rows)
        if out is not sys.stdout:
            out.close()
        self.stdout.write(self.style.SUCCESS("Rapport permissions généré."))
