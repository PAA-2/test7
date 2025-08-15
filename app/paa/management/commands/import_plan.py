from django.core.management.base import BaseCommand

from paa.models import Plan
from paa.models_import import ImportProfile
from paa.importer import import_plan_from_excel


class Command(BaseCommand):
    help = "Importe un plan depuis un fichier Excel"

    def add_arguments(self, parser):
        parser.add_argument("plan_code", type=str, help="Code du plan à importer")
        parser.add_argument("file_path", type=str, help="Chemin du fichier Excel")

    def handle(self, *args, **options):
        plan = Plan.objects.get(code=options["plan_code"])
        profile = ImportProfile.objects.first()
        report = import_plan_from_excel(plan, options["file_path"], profile)
        self.stdout.write(
            self.style.SUCCESS(
                f"Import terminé : {report.created_count} créés, {report.updated_count} MAJ, {report.skipped_count} ignorés"
            )
        )
