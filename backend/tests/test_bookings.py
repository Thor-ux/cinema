import base64


def _book(client, headers, session_id, seat_ids, name="Ann"):
    return client.post("/bookings", json={"session_id": session_id, "seat_ids": seat_ids, "customer_name": name},
                       headers=headers)


def test_booking_requires_login(client, showing):
    res = _book(client, {}, showing["session"]["id"], [showing["seats"][0]["id"]])
    assert res.status_code == 401


def test_booking_prices_tickets_and_creates_qr_codes(client, user_headers, showing):
    standard = next(s for s in showing["seats"] if s["type"] == "standard")
    vip = next(s for s in showing["seats"] if s["type"] == "vip")

    res = _book(client, user_headers, showing["session"]["id"], [standard["id"], vip["id"]])
    assert res.status_code == 201, res.text
    booking = res.json()

    prices = {t["seat_type"]: t["price"] for t in booking["tickets"]}
    assert prices == {"standard": 500.0, "vip": 1000.0}
    assert booking["total_price"] == 1500.0
    assert booking["movie_title"] == "Test Movie"
    assert len(booking["booking_code"]) == 8
    for ticket in booking["tickets"]:
        png = base64.b64decode(ticket["qr_code"])
        assert png.startswith(b"\x89PNG")


def test_booked_seats_show_as_reserved(client, user_headers, showing):
    seat = showing["seats"][5]
    _book(client, user_headers, showing["session"]["id"], [seat["id"]])
    seats = client.get(f"/sessions/{showing['session']['id']}/seats").json()
    reserved = [s["id"] for s in seats if s["is_reserved"]]
    assert reserved == [seat["id"]]


def test_same_seat_cannot_be_booked_twice(client, user_headers, make_user, showing):
    seat_id = showing["seats"][0]["id"]
    assert _book(client, user_headers, showing["session"]["id"], [seat_id]).status_code == 201

    other = make_user("other@example.com")
    res = _book(client, other, showing["session"]["id"], [seat_id, showing["seats"][1]["id"]])
    assert res.status_code == 409
    # The failed booking must not have reserved the free seat either.
    seats = client.get(f"/sessions/{showing['session']['id']}/seats").json()
    assert sum(s["is_reserved"] for s in seats) == 1


def test_database_constraint_stops_double_booking_race(db, showing):
    """Even if two requests both pass the 'is it free?' check, the unique
    constraint on (session_id, seat_id) lets only one of them commit."""
    import pytest
    from sqlalchemy.exc import IntegrityError

    from app.models import Booking, Ticket

    session_id, seat_id = showing["session"]["id"], showing["seats"][0]["id"]
    with db() as s:
        for code in ("AAAA1111", "BBBB2222"):
            b = Booking(session_id=session_id, user_id=1, customer_name="x", booking_code=code)
            s.add(b)
            s.flush()
            s.add(Ticket(booking_id=b.id, session_id=session_id, seat_id=seat_id, price=1, qr_code="x"))
        with pytest.raises(IntegrityError):
            s.commit()


def test_seat_from_another_hall_is_rejected(client, admin_headers, user_headers, showing):
    other = client.post("/admin/halls", json={"name": "Hall B", "rows": 1, "seats_per_row": 1},
                        headers=admin_headers).json()
    assert other["total_seats"] == 1
    foreign_seat_id = max(s["id"] for s in showing["seats"]) + 1  # Hall B's only seat
    res = _book(client, user_headers, showing["session"]["id"], [foreign_seat_id])
    assert res.status_code == 400


def test_invalid_booking_requests(client, user_headers, showing):
    sid, seat_id = showing["session"]["id"], showing["seats"][0]["id"]
    assert _book(client, user_headers, 999, [seat_id]).status_code == 404
    assert _book(client, user_headers, sid, []).status_code == 422
    assert _book(client, user_headers, sid, [seat_id, seat_id]).status_code == 400
    assert _book(client, user_headers, sid, list(range(1, 12))).status_code == 422  # more than 10 seats
    assert _book(client, user_headers, sid, [seat_id], name="").status_code == 422


def test_my_bookings_only_shows_own_bookings(client, user_headers, make_user, showing):
    sid = showing["session"]["id"]
    _book(client, user_headers, sid, [showing["seats"][0]["id"]], name="Ann")
    other = make_user("bob@example.com")
    _book(client, other, sid, [showing["seats"][1]["id"]], name="Bob")

    mine = client.get("/bookings/me", headers=user_headers).json()
    assert [b["customer_name"] for b in mine] == ["Ann"]
    assert client.get("/bookings/me").status_code == 401


def test_admin_sees_all_bookings(client, admin_headers, user_headers, make_user, showing):
    sid = showing["session"]["id"]
    _book(client, user_headers, sid, [showing["seats"][0]["id"]], name="Ann")
    _book(client, make_user("bob@example.com"), sid, [showing["seats"][1]["id"]], name="Bob")
    names = {b["customer_name"] for b in client.get("/admin/bookings", headers=admin_headers).json()}
    assert names == {"Ann", "Bob"}
