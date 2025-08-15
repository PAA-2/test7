from django.core.management.base import BaseCommand
from django.db import connection
from paa.models import Action


class Command(BaseCommand):
    help = "Recalcule le tsvector pour toutes les actions (full-text)."

    def handle(self, *args, **options):
        count = 0
        with connection.cursor() as cur:
            for a_id in Action.objects.values_list("id", flat=True):
                cur.execute("SELECT paa_update_action_search_vector(%s)", [str(a_id)])
                count += 1
        self.stdout.write(
            self.style.SUCCESS(f"Réindexation terminée : {count} actions")
        )
