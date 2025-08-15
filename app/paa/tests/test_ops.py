import pytest


@pytest.mark.django_db
def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json().get("ok") is True


@pytest.mark.django_db
def test_readyz(client):
    resp = client.get("/readyz")
    assert resp.status_code in (200, 503)
    data = resp.json()
    assert "db" in data and "cache" in data


@pytest.mark.django_db
def test_metrics(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"paa_http_requests_total" in resp.content
