import pytest
from django.core.cache import cache
from paa.kpis import get_kpis_cached
from paa.cache_utils import KPI_CACHE_KEY


@pytest.mark.django_db
def test_kpis_cached():
    cache.delete(KPI_CACHE_KEY)
    k1 = get_kpis_cached()
    k2 = get_kpis_cached()
    assert k1 == k2
