# Admin reset-data endpoint (run LAST - wipes txn data and re-seeds)
class TestAdminReset:
    def test_reset_restores_pristine_state(self, base_url, admin):
        r = admin.post(f"{base_url}/api/admin/reset-data", timeout=120)
        assert r.status_code == 200, r.text
        products = admin.get(f"{base_url}/api/products", timeout=30).json()
        assert len(products) == 31, len(products)
        assert len(admin.get(f"{base_url}/api/suppliers", timeout=30).json()) == 7
        assert admin.get(f"{base_url}/api/transactions", timeout=30).json() == []
        assert admin.get(f"{base_url}/api/surat-jalan", timeout=30).json() == []
        assert admin.get(f"{base_url}/api/purchase-orders", timeout=30).json() == []
        assert [p for p in products if p["sku"] == "B0010152Z"][0]["stock"] == 70089
