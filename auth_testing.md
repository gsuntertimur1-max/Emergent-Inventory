# Auth Testing Playbook

## JWT custom auth
Step 1: MongoDB Verification
```
mongosh
use test_database
db.users.find({role: "Administrator"}).pretty()
```
Verify: bcrypt hash starts with `$2b$`, unique index on users.username.

Step 2: API Testing (username-based login)
```
API_URL=$(grep REACT_APP_BACKEND_URL /app/frontend/.env | cut -d '=' -f2)
TOKEN=$(curl -s -X POST "$API_URL/api/auth/login" -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
curl -s "$API_URL/api/auth/me" -H "Authorization: Bearer $TOKEN"
```

## Emergent Google Auth testing
Create test user & session directly in MongoDB:
```
mongosh --eval "
use('test_database');
var userId = 'testuser' + Date.now();
var sessionToken = 'test_session_' + Date.now();
db.users.insertOne({id: userId, username: 'test.google@example.com', email: 'test.google@example.com', name: 'Test Google User', role: 'Pemantau', active: true, auth_provider: 'google', created_at: new Date().toISOString()});
db.user_sessions.insertOne({user_id: userId, session_token: sessionToken, expires_at: new Date(Date.now() + 7*24*60*60*1000).toISOString(), created_at: new Date().toISOString()});
print('Session token: ' + sessionToken);
"
```
Then: `curl "$API_URL/api/auth/me" -H "Authorization: Bearer <sessionToken>"`

Frontend stores token in localStorage key `bulog_token`, sent as Bearer header.
Cannot test real Google OAuth login flow in automation — use the MongoDB session injection above.
