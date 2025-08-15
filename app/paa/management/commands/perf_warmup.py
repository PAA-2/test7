from django.core.management.base import BaseCommand
from paa.tasks_perf import warm_kpi_cache, refresh_consolidated_mv


class Command(BaseCommand):
    help = "Réchauffe le cache KPI et rafraîchit la vue matérialisée."

    def handle(self, *args, **options):
        refresh_consolidated_mv.delay()
        warm_kpi_cache.delay()
        self.stdout.write(self.style.SUCCESS("Warmup & refresh lancés."))
