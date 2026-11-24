import pytest


ADMIN_ROUTES = [
    ("get", "/admin/dashboard"),
    ("get", "/admin/bookings"),
    ("get", "/admin/sessions"),
    ("get", "/admin/halls"),
    ("post", "/admin/movies"),
    ("post", "/admin/halls"),
    ("post", "/admin/sessions"),
]


@pytest.mark.parametrize("method,path", ADMIN_ROUTES)
def test_admin_routes_reject_anonymous_and_regular_users(client, user_headers, method, path):
    assert getattr(client, method)(path).status_code == 401
    assert getattr(client, method)(path, headers=user_headers).status_code == 403


def test_movie_crud(client, admin_headers):
    res = client.post("/admin/movies", json={"title": "Dune", "duration_minutes": 155}, headers=admin_headers)
    assert res.status_code == 201
    movie_id = res.json()["id"]

    assert client.get("/movies").json()[0]["title"] == "Dune"

    res = client.put(f"/admin/movies/{movie_id}", json={"title": "Dune: Part One", "duration_minutes": 155},
                     headers=admin_headers)
    assert res.json()["title"] == "Dune: Part One"

    assert client.delete(f"/admin/movies/{movie_id}", headers=admin_headers).status_code == 204
    assert client.get(f"/movies/{movie_id}").status_code == 404


def test_movie_validation(client, admin_headers):
    bad = [{"title": "", "duration_minutes": 90}, {"title": "X", "duration_minutes": 0},
           {"title": "X", "duration_minutes": 600}]
    for body in bad:
        assert client.post("/admin/movies", json=body, headers=admin_headers).status_code == 422


def test_create_hall_generates_seats_with_vip(client, showing):
    seats = showing["seats"]
    assert len(seats) == 12
    assert showing["hall"] == {"hall_id": showing["hall"]["hall_id"], "total_seats": 12, "vip_seats": 4}
    assert {s["type"] for s in seats if s["row"] == 3} == {"vip"}
    assert {s["type"] for s in seats if s["row"] < 3} == {"standard"}


def test_hall_rejects_vip_seat_outside_hall(client, admin_headers):
    res = client.post("/admin/halls", json={"name": "H", "rows": 2, "seats_per_row": 2,
                                            "vip_seats": [{"row": 3, "number": 1}]}, headers=admin_headers)
    assert res.status_code == 422


def test_session_overlap_in_same_hall_is_refused(client, admin_headers, showing):
    overlapping = showing["start"].replace(hour=20)  # first session runs 19:00–21:00
    body = {"movie_id": showing["movie"]["id"], "hall_id": showing["hall"]["hall_id"],
            "start_time": overlapping.isoformat(), "price": 300}
    assert client.post("/admin/sessions", json=body, headers=admin_headers).status_code == 409

    body["start_time"] = showing["start"].replace(hour=21, minute=30).isoformat()
    assert client.post("/admin/sessions", json=body, headers=admin_headers).status_code == 201


def test_session_needs_existing_movie_and_hall(client, admin_headers, showing):
    body = {"movie_id": 999, "hall_id": showing["hall"]["hall_id"],
            "start_time": showing["start"].isoformat(), "price": 300}
    assert client.post("/admin/sessions", json=body, headers=admin_headers).status_code == 404
    body.update(movie_id=showing["movie"]["id"], hall_id=999)
    assert client.post("/admin/sessions", json=body, headers=admin_headers).status_code == 404


def test_update_price_and_bulk_price(client, admin_headers, showing):
    sid = showing["session"]["id"]
    res = client.patch(f"/admin/sessions/{sid}/price", params={"price": 650}, headers=admin_headers)
    assert res.status_code == 200 and res.json()["price"] == 650
    assert client.patch(f"/admin/sessions/{sid}/price", params={"price": -5}, headers=admin_headers).status_code == 422

    res = client.patch("/admin/sessions/price/bulk", params={"price": 700, "movie_id": showing["movie"]["id"]},
                       headers=admin_headers)
    assert res.json() == {"updated": 1}
    assert client.get(f"/sessions/{sid}").json()["price"] == 700
    assert client.patch("/admin/sessions/price/bulk", params={"price": 700}, headers=admin_headers).status_code == 400


def test_closed_hall_cannot_get_new_sessions(client, admin_headers, showing):
    hall_id = showing["hall"]["hall_id"]
    assert client.patch(f"/admin/halls/{hall_id}", json={"is_active": False}, headers=admin_headers).json()["is_active"] is False
    body = {"movie_id": showing["movie"]["id"], "hall_id": hall_id,
            "start_time": showing["start"].replace(hour=10).isoformat(), "price": 300}
    assert client.post("/admin/sessions", json=body, headers=admin_headers).status_code == 400


def test_dashboard_counts_revenue(client, admin_headers, user_headers, showing):
    seat = showing["seats"][0]
    client.post("/bookings", json={"session_id": showing["session"]["id"], "seat_ids": [seat["id"]],
                                   "customer_name": "Ann"}, headers=user_headers)
    stats = client.get("/admin/dashboard", headers=admin_headers).json()
    assert stats == {"movies": 1, "sessions": 1, "bookings": 1, "tickets_sold": 1, "revenue": 500.0}


def test_cannot_delete_things_that_have_bookings(client, admin_headers, user_headers, showing):
    seat = showing["seats"][0]
    client.post("/bookings", json={"session_id": showing["session"]["id"], "seat_ids": [seat["id"]],
                                   "customer_name": "Ann"}, headers=user_headers)
    assert client.delete(f"/admin/sessions/{showing['session']['id']}", headers=admin_headers).status_code == 409
    assert client.delete(f"/admin/movies/{showing['movie']['id']}", headers=admin_headers).status_code == 409
    assert client.delete(f"/admin/halls/{showing['hall']['hall_id']}", headers=admin_headers).status_code == 409
