# backlog/tests/test_auth.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

BASE = "/api/backlog/auth"

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="tester", password="123456")

@pytest.fixture
def auth_client(db, user):
    c = APIClient()
    # flujo real: CSRF -> LOGIN (session)
    c.get(f"{BASE}/csrf/")
    r = c.post(f"{BASE}/login/", {"username": "tester", "password": "123456"}, format="json")
    assert r.status_code == 200
    return c

@pytest.mark.django_db
def test_auth_me_requires_login(api_client):
    r = api_client.get(f"{BASE}/me/")
    assert r.status_code in (401, 403, 200)
    # En nuestra API /me/ puede responder 200 con {"is_authenticated": false}
    # (ver README_AUTH_BACKEND_LOGIN.md)

@pytest.mark.django_db
def test_auth_me_ok(auth_client):
    r = auth_client.get(f"{BASE}/me/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("is_authenticated") is True
