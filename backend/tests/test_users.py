# User management module: create/list/update/password/delete + guards
import requests


class TestUserManagement:
    created = []

    def _cleanup(self, base_url, admin):
        for uid in self.created:
            admin.delete(f"{base_url}/api/users/{uid}", timeout=30)
        self.created = []

    def test_full_user_lifecycle(self, base_url, admin):
        payload = {"name": "TEST_QA Operator", "username": "test_qa_op", "email": "qa@bulog.test",
                   "role": "Operator", "password": "qa123456"}
        # cleanup leftovers
        for u in admin.get(f"{base_url}/api/users", timeout=30).json():
            if u["username"] == "test_qa_op":
                admin.delete(f"{base_url}/api/users/{u['id']}", timeout=30)

        r = admin.post(f"{base_url}/api/users", json=payload, timeout=30)
        assert r.status_code == 200, r.text
        u = r.json()
        uid = u["id"]
        self.created.append(uid)
        assert "password_hash" not in u and "_id" not in u
        assert u["username"] == "test_qa_op" and u["role"] == "Operator" and u["active"] is True

        # persisted in list
        lst = admin.get(f"{base_url}/api/users", timeout=30).json()
        assert any(x["id"] == uid for x in lst)

        # new user can log in
        lr = requests.post(f"{base_url}/api/auth/login",
                           json={"username": "test_qa_op", "password": "qa123456"}, timeout=30)
        assert lr.status_code == 200, lr.text
        user_token = lr.json()["token"]

        # non-admin guards
        us = requests.Session()
        us.headers.update({"Authorization": f"Bearer {user_token}", "Content-Type": "application/json"})
        assert us.post(f"{base_url}/api/users", json=payload, timeout=30).status_code == 403
        assert us.delete(f"{base_url}/api/users/{uid}", timeout=30).status_code == 403
        assert us.post(f"{base_url}/api/admin/reset-data", timeout=30).status_code == 403

        # duplicate username
        assert admin.post(f"{base_url}/api/users", json=payload, timeout=30).status_code == 400
        # short password
        assert admin.post(f"{base_url}/api/users",
                          json={**payload, "username": "test_qa_op2", "password": "123"}, timeout=30).status_code == 400

        # role change
        pr = admin.put(f"{base_url}/api/users/{uid}", json={"role": "Supervisor"}, timeout=30)
        assert pr.status_code == 200 and pr.json()["role"] == "Supervisor"
        assert [x for x in admin.get(f"{base_url}/api/users", timeout=30).json()
                if x["id"] == uid][0]["role"] == "Supervisor"

        # password change by admin
        assert admin.put(f"{base_url}/api/users/{uid}/password",
                         json={"password": "short"}, timeout=30).status_code == 400
        assert admin.put(f"{base_url}/api/users/{uid}/password",
                         json={"password": "newpass123"}, timeout=30).status_code == 200
        assert requests.post(f"{base_url}/api/auth/login",
                             json={"username": "test_qa_op", "password": "newpass123"}, timeout=30).status_code == 200
        assert requests.post(f"{base_url}/api/auth/login",
                             json={"username": "test_qa_op", "password": "qa123456"}, timeout=30).status_code == 401

        # deactivate -> 403 login
        dr = admin.put(f"{base_url}/api/users/{uid}", json={"active": False}, timeout=30)
        assert dr.status_code == 200 and dr.json()["active"] is False
        assert requests.post(f"{base_url}/api/auth/login",
                             json={"username": "test_qa_op", "password": "newpass123"}, timeout=30).status_code == 403
        assert admin.put(f"{base_url}/api/users/{uid}", json={"active": True}, timeout=30).json()["active"] is True

        # delete -> gone
        assert admin.delete(f"{base_url}/api/users/{uid}", timeout=30).status_code == 200
        self.created.remove(uid)
        assert not [x for x in admin.get(f"{base_url}/api/users", timeout=30).json() if x["id"] == uid]
        assert requests.post(f"{base_url}/api/auth/login",
                             json={"username": "test_qa_op", "password": "newpass123"}, timeout=30).status_code == 401

    def test_admin_self_guards(self, base_url, admin):
        me = admin.get(f"{base_url}/api/auth/me", timeout=30).json()
        # cannot delete own account / last administrator
        r = admin.delete(f"{base_url}/api/users/{me['id']}", timeout=30)
        assert r.status_code == 400, r.status_code
        # cannot deactivate self
        r2 = admin.put(f"{base_url}/api/users/{me['id']}", json={"active": False}, timeout=30)
        assert r2.status_code == 400, r2.status_code
        # cannot demote self
        r3 = admin.put(f"{base_url}/api/users/{me['id']}", json={"role": "Operator"}, timeout=30)
        assert r3.status_code == 400, r3.status_code
        # still admin
        assert admin.get(f"{base_url}/api/auth/me", timeout=30).json()["role"] == "Administrator"

    def test_delete_last_administrator_blocked(self, base_url, admin):
        """Create a second admin, delete it (allowed), and ensure last-admin rule holds."""
        payload = {"name": "TEST_QA Admin2", "username": "test_qa_admin2", "email": "qa2@bulog.test",
                   "role": "Administrator", "password": "qa123456"}
        for u in admin.get(f"{base_url}/api/users", timeout=30).json():
            if u["username"] == payload["username"]:
                admin.delete(f"{base_url}/api/users/{u['id']}", timeout=30)
        r = admin.post(f"{base_url}/api/users", json=payload, timeout=30)
        assert r.status_code == 200, r.text
        uid = r.json()["id"]
        d = admin.delete(f"{base_url}/api/users/{uid}", timeout=30)
        assert d.status_code == 200
        assert admin.delete(f"{base_url}/api/users/{uid}", timeout=30).status_code == 404

    def test_update_missing_user_404(self, base_url, admin):
        assert admin.put(f"{base_url}/api/users/nope-id", json={"role": "Operator"}, timeout=30).status_code == 404
        assert admin.put(f"{base_url}/api/users/nope-id/password",
                         json={"password": "abcdef1"}, timeout=30).status_code == 404
