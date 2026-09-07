# RBAC: verify non-admin / read-only roles cannot mutate master data
import requests


class TestRoleWritePermissions:
    def _make_user(self, base_url, admin, role, username):
        for u in admin.get(f"{base_url}/api/users", timeout=30).json():
            if u["username"] == username:
                admin.delete(f"{base_url}/api/users/{u['id']}", timeout=30)
        r = admin.post(f"{base_url}/api/users", json={
            "name": f"TEST_{role}", "username": username, "email": "",
            "role": role, "password": "testpass123"}, timeout=30)
        assert r.status_code == 200, r.text
        tok = requests.post(f"{base_url}/api/auth/login",
                            json={"username": username, "password": "testpass123"}, timeout=30).json()["token"]
        s = requests.Session()
        s.headers.update({"Content-Type": "application/json", "Authorization": f"Bearer {tok}"})
        return r.json()["id"], s

    def test_pemantau_cannot_delete_product(self, base_url, admin):
        uid, s = self._make_user(base_url, admin, "Pemantau", "test_qa_pemantau")
        try:
            p = admin.post(f"{base_url}/api/products",
                           json={"name": "TEST_RBAC PROD", "sku": "TEST_RBAC1", "stock": 1}, timeout=30).json()
            try:
                r = s.delete(f"{base_url}/api/products/{p['id']}", timeout=30)
                assert r.status_code == 403, f"read-only Pemantau deleted a product (status {r.status_code})"
            finally:
                admin.delete(f"{base_url}/api/products/{p['id']}", timeout=30)
        finally:
            admin.delete(f"{base_url}/api/users/{uid}", timeout=30)

    def test_pemantau_cannot_create_transaction(self, base_url, admin):
        uid, s = self._make_user(base_url, admin, "Pemantau", "test_qa_pemantau2")
        try:
            prod = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
            r = s.post(f"{base_url}/api/transactions", json={
                "type": "MASUK", "items": [{"productId": prod["id"], "qty": 1}], "kondisi": "BAIK"}, timeout=30)
            assert r.status_code == 403, f"read-only Pemantau created a stock transaction (status {r.status_code})"
        finally:
            admin.delete(f"{base_url}/api/users/{uid}", timeout=30)
