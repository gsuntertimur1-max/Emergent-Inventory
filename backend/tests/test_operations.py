# Transactions, surat jalan, purchase orders, CSV import
import io


class TestTransactions:
    def test_masuk_increases_stock(self, base_url, admin):
        products = admin.get(f"{base_url}/api/products", timeout=30).json()
        p = products[0]
        before = p["stock"]
        r = admin.post(f"{base_url}/api/transactions", json={
            "type": "MASUK", "items": [{"productId": p["id"], "qty": 25}],
            "party": "TEST_Supplier", "ref": "TEST_IN_1", "kondisi": "BAIK"}, timeout=30)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["suratJalan"] is None
        assert len(d["transactions"]) == 1 and d["transactions"][0]["change"] == 25
        after = [x for x in admin.get(f"{base_url}/api/products", timeout=30).json() if x["id"] == p["id"]][0]
        assert after["stock"] == before + 25
        txns = admin.get(f"{base_url}/api/transactions", timeout=30).json()
        assert any(t["ref"] == "TEST_IN_1" for t in txns)
        for t in txns:
            assert "_id" not in t

    def test_keluar_creates_surat_jalan_and_status_flow(self, base_url, admin):
        products = admin.get(f"{base_url}/api/products", timeout=30).json()
        p = [x for x in products if x["stock"] > 100][0]
        before = p["stock"]
        r = admin.post(f"{base_url}/api/transactions", json={
            "type": "KELUAR", "items": [{"productId": p["id"], "qty": 10}],
            "party": "TEST_Penerima", "polisi": "B 1234 TST", "kondisi": "BAIK"}, timeout=30)
        assert r.status_code == 200, r.text
        sj = r.json()["suratJalan"]
        assert sj is not None
        assert sj["no"].startswith("SJ-") and len(sj["no"].split("-")) == 3
        assert sj["antrian"].startswith("A-")
        assert sj["status"] == "Menunggu"
        assert sj["penerima"] == "TEST_Penerima"
        after = [x for x in admin.get(f"{base_url}/api/products", timeout=30).json() if x["id"] == p["id"]][0]
        assert after["stock"] == before - 10

        listed = admin.get(f"{base_url}/api/surat-jalan", timeout=30).json()
        assert any(s["id"] == sj["id"] for s in listed)

        for st in ["Sedang Dimuat", "Selesai"]:
            u = admin.put(f"{base_url}/api/surat-jalan/{sj['id']}/status", json={"status": st}, timeout=30)
            assert u.status_code == 200 and u.json()["status"] == st
        persisted = [s for s in admin.get(f"{base_url}/api/surat-jalan", timeout=30).json() if s["id"] == sj["id"]][0]
        assert persisted["status"] == "Selesai"

    def test_keluar_over_stock_400(self, base_url, admin):
        p = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
        r = admin.post(f"{base_url}/api/transactions", json={
            "type": "KELUAR", "items": [{"productId": p["id"], "qty": p["stock"] + 100000}],
            "party": "TEST", "kondisi": "BAIK"}, timeout=30)
        assert r.status_code == 400, r.status_code
        assert "tidak mencukupi" in r.text.lower()

    def test_invalid_type_and_empty_items(self, base_url, admin):
        p = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
        assert admin.post(f"{base_url}/api/transactions", json={
            "type": "XXX", "items": [{"productId": p["id"], "qty": 1}]}, timeout=30).status_code == 400
        assert admin.post(f"{base_url}/api/transactions", json={
            "type": "MASUK", "items": []}, timeout=30).status_code == 400
        assert admin.post(f"{base_url}/api/transactions", json={
            "type": "MASUK", "items": [{"productId": "missing", "qty": 1}]}, timeout=30).status_code == 404

    def test_negative_qty_masuk(self, base_url, admin):
        """Negative quantity should be rejected (data integrity)."""
        p = admin.get(f"{base_url}/api/products", timeout=30).json()[0]
        r = admin.post(f"{base_url}/api/transactions", json={
            "type": "MASUK", "items": [{"productId": p["id"], "qty": -5}], "kondisi": "BAIK"}, timeout=30)
        assert r.status_code in (400, 422), f"negative qty accepted ({r.status_code})"


class TestPurchaseOrders:
    def test_create_po_sequence(self, base_url, admin):
        body = {"supplier": "SAMARA JAYA", "items": [{"name": "TEST_ITEM", "qty": 5, "cost": 1000}],
                "total": 5000, "status": "Draft"}
        r1 = admin.post(f"{base_url}/api/purchase-orders", json=body, timeout=30)
        assert r1.status_code == 200, r1.text
        no1 = r1.json()["no"]
        assert no1.startswith("PO-")
        seq1 = int(no1.split("-")[-1])
        r2 = admin.post(f"{base_url}/api/purchase-orders", json=body, timeout=30)
        seq2 = int(r2.json()["no"].split("-")[-1])
        assert seq2 == seq1 + 1, f"{no1} then {r2.json()['no']}"
        lst = admin.get(f"{base_url}/api/purchase-orders", timeout=30).json()
        assert any(p["no"] == no1 for p in lst)
        for p in lst:
            assert "_id" not in p


class TestCsvImport:
    def test_import_upsert(self, base_url, admin):
        products = admin.get(f"{base_url}/api/products", timeout=30).json()
        existing = [p for p in products if p["sku"] == "B0010152Z"][0]
        csv_text = (
            "sku;nama;jumlah;kategori;satuan;harga_beli;harga_jual;supplier;lokasi\n"
            f"[B0010152Z];{existing['name']};1.234;Beras;Kg;5000;6000;Manager Pengolahan;GD-1\n"
            "[TESTNEW001];TEST_PRODUK IMPORT;500;Gula;Kg;7000;8000;TEST_SUPPLIER IMPORT;GD-2\n"
        )
        files = {"file": ("TEST_import.csv", io.BytesIO(csv_text.encode("utf-8")), "text/csv")}
        s = admin
        headers = {"Authorization": s.headers["Authorization"]}
        import requests
        r = requests.post(f"{base_url}/api/import/csv", files=files, headers=headers, timeout=60)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["updated"] == 1 and d["inserted"] == 1, d

        after = admin.get(f"{base_url}/api/products", timeout=30).json()
        upd = [p for p in after if p["sku"] == "B0010152Z"][0]
        assert upd["stock"] == 1234
        assert upd["cost"] == 5000
        new = [p for p in after if p["sku"] == "TESTNEW001"]
        assert new and new[0]["stock"] == 500 and new[0]["category"] == "Gula"

        sups = {sp["name"] for sp in admin.get(f"{base_url}/api/suppliers", timeout=30).json()}
        assert "TEST_SUPPLIER IMPORT" in sups

    def test_import_invalid_file(self, base_url, admin):
        import requests
        files = {"file": ("TEST_bad.csv", io.BytesIO(b"garbage,not,semicolon\n1,2,3"), "text/csv")}
        r = requests.post(f"{base_url}/api/import/csv", files=files,
                          headers={"Authorization": admin.headers["Authorization"]}, timeout=60)
        assert r.status_code == 400, r.status_code
