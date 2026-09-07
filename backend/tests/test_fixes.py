# Retest of iteration_1 fixes: RBAC require_write, qty validation, RUSAK KELUAR,
# txn ref format, 404 on unknown delete ids
import re

import pytest
import requests


@pytest.fixture(scope="class")
def pemantau(base_url, admin):
    """Create a read-only Pemantau user and return (session, user_id)."""
    username = "test_qa_ro_pemantau"
    for u in admin.get(f"{base_url}/api/users", timeout=30).json():
        if u["username"] == username:
            admin.delete(f"{base_url}/api/users/{u['id']}", timeout=30)
    r = admin.post(f"{base_url}/api/users", json={
        "name": "TEST_Pemantau RO", "username": username, "email": "",
        "role": "Pemantau", "password": "testpass123"}, timeout=30)
    assert r.status_code == 200, r.text
    uid = r.json()["id"]
    lr = requests.post(f"{base_url}/api/auth/login",
                       json={"username": username, "password": "testpass123"}, timeout=30)
    assert lr.status_code == 200, lr.text
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json",
                      "Authorization": f"Bearer {lr.json()['token']}"})
    yield s
    admin.delete(f"{base_url}/api/users/{uid}", timeout=30)


class TestPemantauReadOnly:
    def test_pemantau_reads_allowed(self, base_url, pemantau):
        for ep in ["/api/products", "/api/suppliers", "/api/transactions",
                   "/api/surat-jalan", "/api/purchase-orders", "/api/auth/me"]:
            r = pemantau.get(f"{base_url}{ep}", timeout=30)
            assert r.status_code == 200, f"{ep} -> {r.status_code} {r.text[:150]}"

    def test_pemantau_writes_forbidden(self, base_url, admin, pemantau):
        prod = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
        sups = admin.get(f"{base_url}/api/suppliers", timeout=30).json()
        sup_id = sups[0]["id"] if sups else "missing"
        sj = admin.get(f"{base_url}/api/surat-jalan", timeout=30).json()
        sj_id = sj[0]["id"] if sj else "missing"

        cases = [
            ("POST", "/api/products", {"name": "TEST_RO", "sku": "TEST_RO1", "stock": 1}),
            ("PUT", f"/api/products/{prod['id']}", {"name": "HACKED"}),
            ("DELETE", f"/api/products/{prod['id']}", None),
            ("POST", "/api/suppliers", {"name": "TEST_RO SUP"}),
            ("PUT", f"/api/suppliers/{sup_id}", {"name": "TEST_RO SUP2"}),
            ("DELETE", f"/api/suppliers/{sup_id}", None),
            ("POST", "/api/transactions", {"type": "MASUK",
                                           "items": [{"productId": prod["id"], "qty": 1}],
                                           "kondisi": "BAIK"}),
            ("PUT", f"/api/surat-jalan/{sj_id}/status", {"status": "Selesai"}),
            ("POST", "/api/purchase-orders", {"supplier": "X", "items": [
                {"name": "i", "qty": 1, "cost": 1}], "total": 1}),
        ]
        failures = []
        for method, ep, body in cases:
            r = pemantau.request(method, f"{base_url}{ep}", json=body, timeout=30)
            if r.status_code != 403:
                failures.append(f"{method} {ep} -> {r.status_code}")
        assert not failures, f"Pemantau not blocked: {failures}"

    def test_pemantau_csv_import_forbidden(self, base_url, pemantau):
        import io
        files = {"file": ("TEST_ro.csv", io.BytesIO(b"sku;nama;jumlah\n[X];Y;1\n"), "text/csv")}
        r = requests.post(f"{base_url}/api/import/csv", files=files,
                          headers={"Authorization": pemantau.headers["Authorization"]}, timeout=60)
        assert r.status_code == 403, r.status_code

    def test_pemantau_cannot_manage_users(self, base_url, pemantau):
        r = pemantau.post(f"{base_url}/api/users", json={
            "name": "x", "username": "test_qa_hack", "role": "Administrator",
            "password": "pw12345678"}, timeout=30)
        assert r.status_code == 403, r.status_code

    def test_product_untouched_after_pemantau_attempts(self, base_url, admin):
        prods = admin.get(f"{base_url}/api/products", timeout=30).json()
        assert prods[0]["name"] != "HACKED"
        assert not any(p["sku"] == "TEST_RO1" for p in prods)


class TestQtyValidation:
    def test_negative_qty_rejected(self, base_url, admin):
        p = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
        before = p["stock"]
        r = admin.post(f"{base_url}/api/transactions", json={
            "type": "MASUK", "items": [{"productId": p["id"], "qty": -5}],
            "kondisi": "BAIK"}, timeout=30)
        assert r.status_code == 422, r.status_code
        after = [x for x in admin.get(f"{base_url}/api/products", timeout=30).json()
                 if x["id"] == p["id"]][0]
        assert after["stock"] == before

    def test_zero_qty_rejected(self, base_url, admin):
        p = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
        r = admin.post(f"{base_url}/api/transactions", json={
            "type": "KELUAR", "items": [{"productId": p["id"], "qty": 0}],
            "kondisi": "BAIK"}, timeout=30)
        assert r.status_code == 422, r.status_code


class TestRusakKeluar:
    def test_rusak_keluar_insufficient_400(self, base_url, admin):
        p = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
        damaged_before = p.get("damaged", 0)
        r = admin.post(f"{base_url}/api/transactions", json={
            "type": "KELUAR", "items": [{"productId": p["id"], "qty": damaged_before + 50}],
            "party": "TEST_RUSAK", "kondisi": "RUSAK"}, timeout=30)
        assert r.status_code == 400, f"{r.status_code} {r.text[:200]}"
        assert "tidak mencukupi" in r.text.lower()
        after = [x for x in admin.get(f"{base_url}/api/products", timeout=30).json()
                 if x["id"] == p["id"]][0]
        assert after.get("damaged", 0) == damaged_before

    def test_rusak_masuk_then_keluar_ok(self, base_url, admin):
        p = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
        d0 = p.get("damaged", 0)
        r = admin.post(f"{base_url}/api/transactions", json={
            "type": "MASUK", "items": [{"productId": p["id"], "qty": 10}],
            "ref": "TEST_RUSAK_IN", "kondisi": "RUSAK"}, timeout=30)
        assert r.status_code == 200, r.text
        mid = [x for x in admin.get(f"{base_url}/api/products", timeout=30).json()
               if x["id"] == p["id"]][0]
        assert mid.get("damaged", 0) == d0 + 10
        r2 = admin.post(f"{base_url}/api/transactions", json={
            "type": "KELUAR", "items": [{"productId": p["id"], "qty": 10}],
            "party": "TEST_RUSAK_OUT", "ref": "TEST_RUSAK_OUT", "kondisi": "RUSAK"}, timeout=30)
        assert r2.status_code == 200, r2.text
        end = [x for x in admin.get(f"{base_url}/api/products", timeout=30).json()
               if x["id"] == p["id"]][0]
        assert end.get("damaged", 0) == d0


class TestRefFormat:
    def test_auto_ref_format(self, base_url, admin):
        p = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
        r = admin.post(f"{base_url}/api/transactions", json={
            "type": "MASUK", "items": [{"productId": p["id"], "qty": 1}],
            "kondisi": "BAIK"}, timeout=30)
        assert r.status_code == 200, r.text
        ref = r.json()["transactions"][0]["ref"]
        assert re.fullmatch(r"IN-\d{8}", ref), f"bad ref format: {ref}"

        p2 = [x for x in admin.get(f"{base_url}/api/products", timeout=30).json()
              if x["stock"] > 50][0]
        r2 = admin.post(f"{base_url}/api/transactions", json={
            "type": "KELUAR", "items": [{"productId": p2["id"], "qty": 1}],
            "party": "TEST_REF", "kondisi": "BAIK"}, timeout=30)
        assert r2.status_code == 200, r2.text
        ref2 = r2.json()["transactions"][0]["ref"]
        assert re.fullmatch(r"OUT-\d{8}", ref2), f"bad ref format: {ref2}"


class TestDelete404:
    def test_delete_unknown_product_404(self, base_url, admin):
        r = admin.delete(f"{base_url}/api/products/does-not-exist", timeout=30)
        assert r.status_code == 404, r.status_code

    def test_delete_unknown_supplier_404(self, base_url, admin):
        r = admin.delete(f"{base_url}/api/suppliers/does-not-exist", timeout=30)
        assert r.status_code == 404, r.status_code

    def test_update_unknown_supplier_404(self, base_url, admin):
        r = admin.put(f"{base_url}/api/suppliers/does-not-exist",
                      json={"name": "TEST_X"}, timeout=30)
        assert r.status_code == 404, r.status_code


class TestCors:
    """Preflight at the public URL is answered by the edge proxy with '*', so the
    app-level CORS policy must be asserted against the app itself (port 8001)."""
    APP_URL = "http://localhost:8001"

    def test_cors_explicit_origin(self, base_url):
        r = requests.options(f"{self.APP_URL}/api/auth/login", headers={
            "Origin": base_url, "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"}, timeout=30)
        assert r.status_code in (200, 204), r.status_code
        assert r.headers.get("access-control-allow-origin") == base_url
        assert r.headers.get("access-control-allow-credentials") == "true"

    def test_cors_rejects_unknown_origin(self):
        r = requests.options(f"{self.APP_URL}/api/auth/login", headers={
            "Origin": "https://evil.example.com", "Access-Control-Request-Method": "POST"},
            timeout=30)
        allow = r.headers.get("access-control-allow-origin")
        assert allow not in ("*", "https://evil.example.com"), allow
