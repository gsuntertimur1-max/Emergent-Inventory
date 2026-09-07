# Master data: products seeded from CSV, suppliers, product CRUD
EXPECTED_CATEGORIES = {"Beras", "Minyak", "Gula", "Tepung", "Sarden", "Teh", "Margarin",
                       "Kecap", "Kopi", "Susu", "Kemasan"}
EXPECTED_SUPPLIERS = {
    "Jasa Prima Logistik", "Manager Pengolahan", "PT Agro Indo Sejahtera",
    "PT Ghendis Multi Manis", "PT Sinar Mas Agro Resources And Technology TBK",
    "RTR DKI Jakarta & Banten", "SAMARA JAYA",
}


class TestProducts:
    def test_products_seeded(self, base_url, admin):
        r = admin.get(f"{base_url}/api/products", timeout=30)
        assert r.status_code == 200
        products = r.json()
        assert len(products) == 31, f"expected 31 products, got {len(products)}"
        for p in products:
            assert "_id" not in p
            assert p["sku"] and "[" not in p["sku"] and "]" not in p["sku"]
        skus = {p["sku"] for p in products}
        assert "B0010152Z" in skus
        cats = {p["category"] for p in products}
        assert cats <= EXPECTED_CATEGORIES, f"unexpected categories {cats - EXPECTED_CATEGORIES}"

    def test_specific_product_stock(self, base_url, admin):
        products = admin.get(f"{base_url}/api/products", timeout=30).json()
        target = [p for p in products if p["sku"] == "B0010152Z"]
        assert target, "seed SKU B0010152Z missing"
        assert target[0]["stock"] == 70089, target[0]["stock"]
        assert target[0]["name"].startswith("BERAS MEDIUM HASIL REPROSES LOGO BANTUAN PANGAN 10 KG")

    def test_product_crud(self, base_url, admin):
        payload = {"name": "TEST_PRODUK QA", "sku": "TEST_SKU_1", "category": "Beras",
                   "stock": 10, "unit": "Kg", "supplier": "SAMARA JAYA"}
        r = admin.post(f"{base_url}/api/products", json=payload, timeout=30)
        assert r.status_code == 200, r.text
        pid = r.json()["id"]
        try:
            got = [p for p in admin.get(f"{base_url}/api/products", timeout=30).json() if p["id"] == pid]
            assert got and got[0]["stock"] == 10
            u = admin.put(f"{base_url}/api/products/{pid}", json={"stock": 55}, timeout=30)
            assert u.status_code == 200 and u.json()["stock"] == 55
            got = [p for p in admin.get(f"{base_url}/api/products", timeout=30).json() if p["id"] == pid]
            assert got[0]["stock"] == 55
        finally:
            d = admin.delete(f"{base_url}/api/products/{pid}", timeout=30)
            assert d.status_code == 200
        assert not [p for p in admin.get(f"{base_url}/api/products", timeout=30).json() if p["id"] == pid]

    def test_update_missing_product_404(self, base_url, admin):
        r = admin.put(f"{base_url}/api/products/does-not-exist", json={"stock": 1}, timeout=30)
        assert r.status_code == 404, r.status_code


class TestSuppliers:
    def test_suppliers_seeded(self, base_url, admin):
        r = admin.get(f"{base_url}/api/suppliers", timeout=30)
        assert r.status_code == 200
        sups = r.json()
        names = {s["name"] for s in sups}
        assert names == EXPECTED_SUPPLIERS, f"diff: {names ^ EXPECTED_SUPPLIERS}"
        assert len(sups) == 7
        for s in sups:
            assert "_id" not in s

    def test_supplier_crud(self, base_url, admin):
        r = admin.post(f"{base_url}/api/suppliers", json={"name": "TEST_SUP QA", "category": "Beras"}, timeout=30)
        assert r.status_code == 200
        sid = r.json()["id"]
        try:
            up = admin.put(f"{base_url}/api/suppliers/{sid}",
                           json={"name": "TEST_SUP QA2", "pic": "Budi", "category": "Gula"}, timeout=30)
            assert up.status_code == 200 and up.json()["pic"] == "Budi"
        finally:
            assert admin.delete(f"{base_url}/api/suppliers/{sid}", timeout=30).status_code == 200
        assert not [s for s in admin.get(f"{base_url}/api/suppliers", timeout=30).json() if s["id"] == sid]
