from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

ROLES = ["SA", "PP", "P", "U"]


class Command(BaseCommand):
    help = "Crée des utilisateurs et groupes de test (SA/PP/P/U) avec mot de passe 'test1234'."

    def handle(self, *args, **options):
        for r in ROLES:
            Group.objects.get_or_create(name=r)
        for r in ROLES:
            u, _ = User.objects.get_or_create(
                username=f"user_{r}",
                defaults={"email": f"{r.lower()}@local", "is_staff": True},
            )
            u.set_password("test1234")
            u.save()
            g = Group.objects.get(name=r)
            u.groups.add(g)
        self.stdout.write(self.style.SUCCESS("Utilisateurs & groupes de test créés."))
