# Auth module: JWT login, /auth/me, logout, guards, google session validation
import requests


class TestAuth:
    def test_root(self, base_url):
        r = requests.get(f"{base_url}/api/", timeout=30)
        assert r.status_code == 200
        assert "message" in r.json()

    def test_login_success(self, base_url, test_credentials):
        r = requests.post(f"{base_url}/api/auth/login", json=test_credentials, timeout=30)
        assert r.status_code == 200, r.text
        d = r.json()
        assert isinstance(d["token"], str) and len(d["token"]) > 20
        assert d["user"]["username"] == "admin"
        assert d["user"]["role"] == "Administrator"
        assert "password_hash" not in d["user"]
        assert "_id" not in d["user"]
        # httpOnly cookie check
        assert "access_token" in r.cookies.get_dict() or "access_token" in r.headers.get("set-cookie", "")

    def test_login_wrong_password(self, base_url):
        r = requests.post(f"{base_url}/api/auth/login", json={"username": "admin", "password": "nope"}, timeout=30)
        assert r.status_code == 401

    def test_login_unknown_user(self, base_url):
        r = requests.post(f"{base_url}/api/auth/login", json={"username": "ghost_x", "password": "x"}, timeout=30)
        assert r.status_code == 401

    def test_login_username_case_insensitive(self, base_url, test_credentials):
        r = requests.post(f"{base_url}/api/auth/login",
                          json={"username": "ADMIN", "password": test_credentials["password"]}, timeout=30)
        assert r.status_code == 200, r.text

    def test_me(self, base_url, admin):
        r = admin.get(f"{base_url}/api/auth/me", timeout=30)
        assert r.status_code == 200
        assert r.json()["username"] == "admin"

    def test_me_bad_token(self, base_url):
        r = requests.get(f"{base_url}/api/auth/me", headers={"Authorization": "Bearer garbage"}, timeout=30)
        assert r.status_code == 401

    def test_brute_force_lockout(self, base_url, clear_login_attempts):
        """Playbook expects lockout after 5 failed attempts (tracked by username)."""
        uname = "test_qa_bruteforce"
        clear_login_attempts(uname)
        codes = []
        for _ in range(7):
            r = requests.post(f"{base_url}/api/auth/login",
                              json={"username": uname, "password": "wrong-pass"}, timeout=30)
            codes.append(r.status_code)
        try:
            assert codes[:5] == [401] * 5, f"expected 5x401 first, got {codes}"
            assert codes[5] == 429 and codes[6] == 429, f"no lockout, codes={codes}"
            body = requests.post(f"{base_url}/api/auth/login",
                                 json={"username": uname, "password": "wrong-pass"}, timeout=30).json()
            assert "Terlalu banyak percobaan" in str(body.get("detail", "")), body
        finally:
            clear_login_attempts(uname)

    def test_admin_still_usable_after_bruteforce(self, base_url, test_credentials, clear_login_attempts):
        clear_login_attempts("admin")
        r = requests.post(f"{base_url}/api/auth/login", json=test_credentials, timeout=30)
        assert r.status_code == 200, r.text


class TestAuthGuards:
    ENDPOINTS = ["/api/products", "/api/suppliers", "/api/transactions",
                 "/api/surat-jalan", "/api/purchase-orders", "/api/users"]

    def test_all_data_endpoints_require_auth(self, base_url):
        for ep in self.ENDPOINTS:
            r = requests.get(f"{base_url}{ep}", timeout=30)
            assert r.status_code == 401, f"{ep} -> {r.status_code}"

    def test_admin_endpoints_require_auth(self, base_url):
        r = requests.post(f"{base_url}/api/admin/reset-data", timeout=30)
        assert r.status_code == 401
