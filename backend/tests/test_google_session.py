# Emergent Google auth: backend session_token validation (session injected into MongoDB)
import os
import subprocess
import time

import pytest
import requests
from dotenv import dotenv_values

BE = dotenv_values("/app/backend/.env")
MONGO_URL = os.environ.get("MONGO_URL") or BE.get("MONGO_URL")
DB_NAME = (os.environ.get("DB_NAME") or BE.get("DB_NAME") or "").strip('"')


def mongosh(js):
    r = subprocess.run(["mongosh", MONGO_URL, "--quiet", "--eval", js],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        pytest.fail(f"mongosh failed: {r.stderr[:400]}")
    return r.stdout.strip()


@pytest.fixture(scope="class")
def google_session():
    stamp = str(int(time.time()))
    uid = f"TESTgoogle{stamp}"
    valid = f"test_session_{stamp}"
    expired = f"test_session_exp_{stamp}"
    js = f"""
    db = db.getSiblingDB('{DB_NAME}');
    db.users.insertOne({{id:'{uid}', username:'test.google{stamp}@example.com',
      email:'test.google{stamp}@example.com', name:'TEST Google User', role:'Pemantau',
      active:true, auth_provider:'google', created_at:new Date().toISOString()}});
    db.user_sessions.insertOne({{user_id:'{uid}', session_token:'{valid}',
      expires_at:new Date(Date.now()+7*24*3600*1000).toISOString(), created_at:new Date().toISOString()}});
    db.user_sessions.insertOne({{user_id:'{uid}', session_token:'{expired}',
      expires_at:new Date(Date.now()-3600*1000).toISOString(), created_at:new Date().toISOString()}});
    print('ok');
    """
    mongosh(js)
    yield {"uid": uid, "valid": valid, "expired": expired,
           "email": f"test.google{stamp}@example.com"}
    mongosh(f"db = db.getSiblingDB('{DB_NAME}'); db.users.deleteMany({{id:'{uid}'}});"
            f"db.user_sessions.deleteMany({{user_id:'{uid}'}}); print('cleaned');")


class TestGoogleSession:
    def test_me_with_session_token(self, base_url, google_session):
        r = requests.get(f"{base_url}/api/auth/me",
                         headers={"Authorization": f"Bearer {google_session['valid']}"}, timeout=30)
        assert r.status_code == 200, r.text
        u = r.json()
        assert u["email"] == google_session["email"]
        assert u["role"] == "Pemantau"
        assert u["auth_provider"] == "google"
        assert "password_hash" not in u and "_id" not in u

    def test_data_endpoint_with_session_token(self, base_url, google_session):
        r = requests.get(f"{base_url}/api/products",
                         headers={"Authorization": f"Bearer {google_session['valid']}"}, timeout=30)
        assert r.status_code == 200
        assert len(r.json()) >= 31

    def test_expired_session_rejected(self, base_url, google_session):
        r = requests.get(f"{base_url}/api/auth/me",
                         headers={"Authorization": f"Bearer {google_session['expired']}"}, timeout=30)
        assert r.status_code == 401, r.status_code

    def test_non_admin_google_user_blocked_from_admin(self, base_url, google_session):
        h = {"Authorization": f"Bearer {google_session['valid']}"}
        assert requests.post(f"{base_url}/api/admin/reset-data", headers=h, timeout=30).status_code == 403
        assert requests.post(f"{base_url}/api/users", json={"name": "x", "username": "y", "password": "abcdef"},
                             headers=h, timeout=30).status_code == 403

    def test_logout_invalidates_session(self, base_url, google_session):
        h = {"Authorization": f"Bearer {google_session['valid']}"}
        assert requests.post(f"{base_url}/api/auth/logout", headers=h, timeout=30).status_code == 200
        assert requests.get(f"{base_url}/api/auth/me", headers=h, timeout=30).status_code == 401

    def test_invalid_session_id_exchange(self, base_url):
        r = requests.post(f"{base_url}/api/auth/session", json={"session_id": "invalid-session-xyz"}, timeout=60)
        assert r.status_code == 401, r.status_code
