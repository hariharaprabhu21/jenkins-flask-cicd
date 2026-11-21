from app import app

def test_home():
    r = app.test_client().get("/")
    assert r.status_code == 200

def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200

def test_version():
    r = app.test_client().get("/version")
    assert r.get_json()["version"] == "2.0"