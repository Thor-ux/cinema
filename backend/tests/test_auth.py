from tests.conftest import USER


def test_register_returns_user_without_password(client):
    res = client.post("/auth/register", json=USER)
    assert res.status_code == 201
    body = res.json()
    assert body["email"] == USER["email"]
    assert body["is_admin"] is False
    assert "password" not in body


def test_register_rejects_duplicate_email_case_insensitive(client):
    client.post("/auth/register", json=USER)
    res = client.post("/auth/register", json={**USER, "email": USER["email"].upper()})
    assert res.status_code == 400


def test_register_validates_email_and_password(client):
    assert client.post("/auth/register", json={"email": "not-an-email", "password": "long-enough-1"}).status_code == 422
    assert client.post("/auth/register", json={"email": "a@example.com", "password": "short"}).status_code == 422


def test_password_is_stored_hashed(client, db):
    from app.models import User

    client.post("/auth/register", json=USER)
    with db() as s:
        stored = s.query(User).one().password
    assert stored != USER["password"]
    assert stored.startswith("$2")  # bcrypt


def test_login_and_me(client):
    client.post("/auth/register", json=USER)
    res = client.post("/auth/login", json=USER)
    assert res.status_code == 200
    token = res.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == USER["email"]


def test_login_wrong_password_and_unknown_email_look_the_same(client):
    client.post("/auth/register", json=USER)
    wrong_pw = client.post("/auth/login", json={**USER, "password": "wrong-password"})
    no_user = client.post("/auth/login", json={"email": "nobody@example.com", "password": "whatever-123"})
    assert wrong_pw.status_code == no_user.status_code == 401
    assert wrong_pw.json() == no_user.json()


def test_protected_route_needs_valid_token(client):
    assert client.get("/auth/me").status_code == 401
    assert client.get("/auth/me", headers={"Authorization": "Bearer not.a.token"}).status_code == 401


def test_expired_token_is_rejected(client, monkeypatch):
    from app.core import security
    from app.core.config import settings

    client.post("/auth/register", json=USER)
    monkeypatch.setattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", -1)
    token = security.create_access_token(1)
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_token_signed_with_other_key_is_rejected(client):
    import jwt

    client.post("/auth/register", json=USER)
    forged = jwt.encode({"sub": "1"}, "some-other-secret-key-that-is-long-enough", algorithm="HS256")
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {forged}"}).status_code == 401
