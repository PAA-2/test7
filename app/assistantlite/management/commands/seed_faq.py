from django.core.management.base import BaseCommand
from assistantlite.models import FAQ

DEFAULTS = [
    (
        "Comment créer une action ?",
        "Tapez: **nouvelle action: <titre>**\nEx: `nouvelle action: Mettre à jour procédure sécurité`.",
    ),
    (
        "Comment demander un check ?",
        "Tapez: **check <CODE_ACTION>**\nEx: `check A12BC34`.",
    ),
    (
        "Comment décaler une échéance ?",
        "Tapez: **delai <CODE_ACTION> +7j** pour +7 jours.",
    ),
    (
        "Comment lancer une synchro Excel ?",
        "Tapez: **sync <CODE_PLAN>**\nEx: `sync P001`.",
    ),
    (
        "Comment exporter les actions ?",
        "Tapez: **export actions** (redirigé vers le CSV).",
    ),
]


class Command(BaseCommand):
    help = "Insère des entrées FAQ par défaut pour l’assistant."

    def handle(self, *args, **kwargs):
        for q, a in DEFAULTS:
            FAQ.objects.get_or_create(question=q, defaults={"answer_md": a})
        self.stdout.write(self.style.SUCCESS("FAQ par défaut insérée."))
