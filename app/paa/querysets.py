from datetime import date
from django.db.models import QuerySet


class ActionQuerySet(QuerySet):
    def fast(self):
        return self.select_related("created_by").prefetch_related("responsables")

    def open(self):
        return self.exclude(status__in=["CLOTUREE", "ARCHIVEE"])

    def overdue(self):
        return self.open().filter(due_date__lt=date.today())
