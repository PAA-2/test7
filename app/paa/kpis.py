from datetime import date, timedelta
from .models import Action
from .cache_utils import cache_get, cache_set, KPI_CACHE_KEY


def compute_kpis():
    total = Action.objects.count()
    en_cours = Action.objects.filter(status="EN_COURS").count()
    en_traitement = Action.objects.filter(status="EN_TRAITEMENT").count()
    retards = Action.objects.open().filter(due_date__lt=date.today()).count()
    cloturees_7j = Action.objects.filter(
        status="CLOTUREE", updated_at__date__gte=(date.today() - timedelta(days=7))
    ).count()
    return {
        "total": total,
        "en_cours": en_cours,
        "en_traitement": en_traitement,
        "retards": retards,
        "cloturees_7j": cloturees_7j,
    }


def get_kpis_cached():
    kpis = cache_get(KPI_CACHE_KEY)
    if kpis is None:
        kpis = compute_kpis()
        cache_set(KPI_CACHE_KEY, kpis)
    return kpis
