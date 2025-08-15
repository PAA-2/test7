from django.db import connections
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time


def healthz(request):
    return JsonResponse({"ok": True, "ts": int(time.time())})


def readyz(request):
    ok_db = ok_cache = True
    try:
        with connections["default"].cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()
    except Exception:
        ok_db = False
    try:
        cache.set("readyz", "1", 5)
        ok_cache = cache.get("readyz") == "1"
    except Exception:
        ok_cache = False
    ok = ok_db and ok_cache
    status = 200 if ok else 503
    return JsonResponse({"ok": ok, "db": ok_db, "cache": ok_cache}, status=status)


def celery_health(request):
    key = "celery:heartbeat"
    hb = cache.get(key)
    ok = bool(hb) and (time.time() - float(hb) < 300)
    return JsonResponse({"ok": ok, "last": hb}, status=200 if ok else 503)


def metrics(request):
    output = generate_latest()
    return HttpResponse(output, content_type=CONTENT_TYPE_LATEST)
