def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_movies_and_showtimes_are_public(client, showing):
    movies = client.get("/movies").json()
    assert [m["title"] for m in movies] == ["Test Movie"]
    showtimes = client.get(f"/movies/{showing['movie']['id']}/showtimes").json()
    assert len(showtimes) == 1 and showtimes[0]["price"] == 500.0


def test_unknown_ids_return_404(client):
    assert client.get("/movies/999").status_code == 404
    assert client.get("/movies/999/showtimes").status_code == 404
    assert client.get("/sessions/999/seats").status_code == 404


def test_cors_allows_configured_frontend_only(client):
    ok = client.options("/movies", headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"})
    assert ok.headers.get("access-control-allow-origin") == "http://localhost:5173"
    bad = client.options("/movies", headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "GET"})
    assert "access-control-allow-origin" not in bad.headers
