import os
import re
from pathlib import Path

import pytest
import requests
from dotenv import dotenv_values

frontend_env = dotenv_values("/app/frontend/.env")
_base = os.environ.get("REACT_APP_BACKEND_URL") or frontend_env.get("REACT_APP_BACKEND_URL")
if not _base:
    raise RuntimeError("REACT_APP_BACKEND_URL missing")
BASE_URL = _base.rstrip("/")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def test_credentials():
    p = Path("/app/memory/test_credentials.md")
    if not p.exists():
        pytest.skip("missing test_credentials.md")
    content = p.read_text(encoding="utf-8")
    u = re.search(r"(?im)^\s*[-*]?\s*(?:\*\*)?Username(?:\*\*)?\s*:\s*`?([^`\s]+)", content)
    pw = re.search(r"(?im)^\s*[-*]?\s*(?:\*\*)?Password(?:\*\*)?\s*:\s*`?([^`\s]+)", content)
    if not u or not pw:
        pytest.skip("no creds in test_credentials.md")
    return {"username": u.group(1), "password": pw.group(1)}


@pytest.fixture(scope="class")
def api_client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="class")
def admin_token(test_credentials):
    r = requests.post(f"{BASE_URL}/api/auth/login", json=test_credentials, timeout=30)
    if r.status_code != 200:
        pytest.fail(f"admin login failed {r.status_code}: {r.text[:300]}")
    tok = r.json().get("token")
    if not tok:
        pytest.fail("no token in login response")
    return tok


@pytest.fixture(scope="session")
def clear_login_attempts():
    """Remove brute-force counters directly from Mongo so tests don't lock accounts."""
    backend_env = dotenv_values("/app/backend/.env")
    mongo_url = os.environ.get("MONGO_URL") or backend_env.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME") or backend_env.get("DB_NAME")
    from pymongo import MongoClient
    client = MongoClient(mongo_url)
    coll = client[db_name].login_attempts

    def _clear(identifier=None):
        if identifier:
            coll.delete_many({"identifier": identifier})
        else:
            coll.delete_many({})
    yield _clear
    _clear()
    client.close()


@pytest.fixture(scope="class")
def admin(admin_token):
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json", "Authorization": f"Bearer {admin_token}"})
    return s
