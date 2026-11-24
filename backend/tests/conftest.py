import os

# Settings are read at import time, so set them before importing the app.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-key-that-is-long-enough-for-hs256"

from datetime import datetime, timedelta, timezone  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.database import Base  # noqa: E402
from app.dependencies.db import get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import User  # noqa: E402
from app.core.security import hash_password  # noqa: E402

ADMIN = {"email": "admin@example.com", "password": "admin-pass-123"}
USER = {"email": "user@example.com", "password": "user-pass-123"}


@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False)
    session = TestingSession()
    yield TestingSession
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(db):
    def override_get_db():
        session = db()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def _token(client, creds):
    res = client.post("/auth/login", json=creds)
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


@pytest.fixture
def admin_headers(client, db):
    with db() as s:
        s.add(User(email=ADMIN["email"], password=hash_password(ADMIN["password"]), is_admin=True))
        s.commit()
    return _token(client, ADMIN)


@pytest.fixture
def user_headers(client):
    assert client.post("/auth/register", json=USER).status_code == 201
    return _token(client, USER)


@pytest.fixture
def make_user(client):
    """Register and log in an extra user; returns auth headers."""
    def _make(email):
        creds = {"email": email, "password": "another-pass-123"}
        assert client.post("/auth/register", json=creds).status_code == 201
        return _token(client, creds)
    return _make


@pytest.fixture
def showing(client, admin_headers):
    """A movie, a 3x4 hall with VIP seats in row 3, and one session at 500.0."""
    movie = client.post(
        "/admin/movies",
        json={"title": "Test Movie", "description": "A test", "duration_minutes": 120},
        headers=admin_headers,
    ).json()
    hall = client.post(
        "/admin/halls",
        json={"name": "Hall A", "rows": 3, "seats_per_row": 4,
              "vip_seats": [{"row": 3, "number": n} for n in range(1, 5)]},
        headers=admin_headers,
    ).json()
    start = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=19, minute=0, second=0, microsecond=0)
    session = client.post(
        "/admin/sessions",
        json={"movie_id": movie["id"], "hall_id": hall["hall_id"], "start_time": start.isoformat(), "price": 500.0},
        headers=admin_headers,
    ).json()
    seats = client.get(f"/sessions/{session['id']}/seats").json()
    return {"movie": movie, "hall": hall, "session": session, "seats": seats, "start": start}
