from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "VACUUM (FULL optionnel) & ANALYZE des tables principales."

    def add_arguments(self, parser):
        parser.add_argument("--full", action="store_true", help="VACUUM FULL")

    def handle(self, *args, **opts):
        stmts = [
            f"VACUUM {'FULL' if opts['full'] else ''} ANALYZE paa_action;",
            f"VACUUM {'FULL' if opts['full'] else ''} ANALYZE paa_plan;",
            f"VACUUM {'FULL' if opts['full'] else ''} ANALYZE paa_actionplan;",
        ]
        with connection.cursor() as cur:
            for s in stmts:
                cur.execute(s)
        self.stdout.write(self.style.SUCCESS("VACUUM/ANALYZE effectué."))
