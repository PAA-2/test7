from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = "Vide le cache applicatif."

    def handle(self, *args, **opts):
        cache.clear()
        self.stdout.write(self.style.SUCCESS("Cache vidé."))
