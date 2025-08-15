from celery import shared_task
from django.db import connection
from .kpis import compute_kpis
from .cache_utils import cache_set, KPI_CACHE_KEY


@shared_task
def refresh_consolidated_mv():
    with connection.cursor() as cur:
        cur.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_plan_consolidated;")
    return "ok"


@shared_task
def warm_kpi_cache():
    cache_set(KPI_CACHE_KEY, compute_kpis())
    return "ok"
