from django.core.cache import cache

KPI_CACHE_KEY = "kpis:v1"
KPI_TTL = 60


def cache_get(key, default=None):
    return cache.get(key, default)


def cache_set(key, value, ttl=None):
    cache.set(key, value, ttl or KPI_TTL)


def invalidate_key(key):
    cache.delete(key)
