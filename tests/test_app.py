from app.main import app


def test_health():
    client = app.test_client()
    r = client.get('/health')
    assert r.status_code == 200
    assert r.get_json()['status'] == 'ok'


def test_summary_has_total():
    client = app.test_client()
    r = client.get('/incidents/summary')
    assert r.status_code == 200
    assert 'total' in r.get_json()


def test_metrics_exposed():
    client = app.test_client()
    r = client.get('/metrics')
    assert b'servicenow_open_incidents' in r.data