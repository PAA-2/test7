import time
from celery import shared_task
from django.core.cache import cache
from prometheus_client import Counter

TASK_OK = Counter("paa_celery_task_success_total", "Celery task successes", ["task"])
TASK_KO = Counter("paa_celery_task_fail_total", "Celery task failures", ["task"])


@shared_task(bind=True)
def celery_heartbeat(self):
    cache.set("celery:heartbeat", str(time.time()), 300)
    TASK_OK.labels("celery_heartbeat").inc()
    return "ok"


def instrumented(task_fn):
    def _wrap(*args, **kwargs):
        name = getattr(task_fn, "__name__", "task")
        try:
            res = task_fn(*args, **kwargs)
            TASK_OK.labels(name).inc()
            return res
        except Exception:
            TASK_KO.labels(name).inc()
            raise

    return _wrap
