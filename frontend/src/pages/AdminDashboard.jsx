import { useCallback, useEffect, useState } from "react";
import { api, formatPrice, formatTime } from "../api/client";

const emptySession = { movie_id: "", hall_id: "", start_time: "", price: "" };
const emptyMovie = { title: "", description: "", duration_minutes: "" };
const emptyHall = { name: "", rows: "", seats_per_row: "", vip_rows: "" };

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [movies, setMovies] = useState([]);
  const [halls, setHalls] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [movieForm, setMovieForm] = useState(emptyMovie);
  const [hallForm, setHallForm] = useState(emptyHall);
  const [sessionForm, setSessionForm] = useState(emptySession);
  const [prices, setPrices] = useState({});
  const [message, setMessage] = useState(null);

  const load = useCallback(async () => {
    const [s, m, h, ss, b] = await Promise.all([
      api("/admin/dashboard"), api("/movies"), api("/admin/halls"), api("/admin/sessions"), api("/admin/bookings"),
    ]);
    setStats(s); setMovies(m); setHalls(h); setSessions(ss); setBookings(b);
  }, []);

  useEffect(() => {
    load().catch((e) => setMessage({ error: e.message }));
  }, [load]);

  // Run an admin action, show its result, then reload everything.
  const run = async (action, success) => {
    setMessage(null);
    try {
      await action();
      setMessage({ ok: success });
      await load();
      return true;
    } catch (e) {
      setMessage({ error: e.message });
      return false;
    }
  };

  const movieTitle = (id) => movies.find((m) => m.id === id)?.title ?? `Movie ${id}`;
  const hallName = (id) => halls.find((h) => h.id === id)?.name ?? `Hall ${id}`;

  const createMovie = async (e) => {
    e.preventDefault();
    const body = { ...movieForm, duration_minutes: Number(movieForm.duration_minutes), description: movieForm.description || null };
    if (await run(() => api("/admin/movies", { method: "POST", body }), "Movie added")) setMovieForm(emptyMovie);
  };

  const createHall = async (e) => {
    e.preventDefault();
    const rows = Number(hallForm.rows), perRow = Number(hallForm.seats_per_row);
    const vipRows = hallForm.vip_rows.split(",").map((x) => Number(x.trim())).filter((x) => x > 0 && x <= rows);
    const vip_seats = vipRows.flatMap((row) => Array.from({ length: perRow }, (_, i) => ({ row, number: i + 1 })));
    const body = { name: hallForm.name, rows, seats_per_row: perRow, vip_seats };
    if (await run(() => api("/admin/halls", { method: "POST", body }), "Hall added")) setHallForm(emptyHall);
  };

  const createSession = async (e) => {
    e.preventDefault();
    const body = {
      movie_id: Number(sessionForm.movie_id),
      hall_id: Number(sessionForm.hall_id),
      start_time: new Date(sessionForm.start_time).toISOString(),
      price: Number(sessionForm.price),
    };
    if (await run(() => api("/admin/sessions", { method: "POST", body }), "Session added")) setSessionForm(emptySession);
  };

  const updatePrice = (id) =>
    run(() => api(`/admin/sessions/${id}/price`, { method: "PATCH", params: { price: prices[id] } }), "Price updated");

  const deleteSession = (id) =>
    window.confirm("Delete this session?") && run(() => api(`/admin/sessions/${id}`, { method: "DELETE" }), "Session deleted");

  const toggleHall = (hall) =>
    run(() => api(`/admin/halls/${hall.id}`, { method: "PATCH", body: { is_active: !hall.is_active } }),
      hall.is_active ? "Hall closed" : "Hall reopened");

  return (
    <>
      <h1>Admin</h1>
      {message?.error && <p className="error">{message.error}</p>}
      {message?.ok && <p className="success">{message.ok}</p>}

      {stats && (
        <div className="stats">
          <div className="card"><span className="muted">Movies</span><strong>{stats.movies}</strong></div>
          <div className="card"><span className="muted">Sessions</span><strong>{stats.sessions}</strong></div>
          <div className="card"><span className="muted">Bookings</span><strong>{stats.bookings}</strong></div>
          <div className="card"><span className="muted">Tickets sold</span><strong>{stats.tickets_sold}</strong></div>
          <div className="card"><span className="muted">Revenue</span><strong>{formatPrice(stats.revenue)}</strong></div>
        </div>
      )}

      <div className="admin-forms">
        <form className="card form" onSubmit={createMovie}>
          <h3>Add movie</h3>
          <input placeholder="Title" required value={movieForm.title} onChange={(e) => setMovieForm({ ...movieForm, title: e.target.value })} />
          <input placeholder="Duration (minutes)" type="number" min="1" max="499" required value={movieForm.duration_minutes}
            onChange={(e) => setMovieForm({ ...movieForm, duration_minutes: e.target.value })} />
          <textarea placeholder="Description" rows="2" value={movieForm.description}
            onChange={(e) => setMovieForm({ ...movieForm, description: e.target.value })} />
          <button className="btn">Add movie</button>
        </form>

        <form className="card form" onSubmit={createHall}>
          <h3>Add hall</h3>
          <input placeholder="Name" required value={hallForm.name} onChange={(e) => setHallForm({ ...hallForm, name: e.target.value })} />
          <div className="two">
            <input placeholder="Rows" type="number" min="1" max="50" required value={hallForm.rows}
              onChange={(e) => setHallForm({ ...hallForm, rows: e.target.value })} />
            <input placeholder="Seats per row" type="number" min="1" max="60" required value={hallForm.seats_per_row}
              onChange={(e) => setHallForm({ ...hallForm, seats_per_row: e.target.value })} />
          </div>
          <input placeholder="VIP rows, e.g. 7, 8" value={hallForm.vip_rows} onChange={(e) => setHallForm({ ...hallForm, vip_rows: e.target.value })} />
          <button className="btn">Add hall</button>
        </form>

        <form className="card form" onSubmit={createSession}>
          <h3>Add session</h3>
          <select required value={sessionForm.movie_id} onChange={(e) => setSessionForm({ ...sessionForm, movie_id: e.target.value })}>
            <option value="">Movie…</option>
            {movies.map((m) => <option key={m.id} value={m.id}>{m.title}</option>)}
          </select>
          <select required value={sessionForm.hall_id} onChange={(e) => setSessionForm({ ...sessionForm, hall_id: e.target.value })}>
            <option value="">Hall…</option>
            {halls.filter((h) => h.is_active).map((h) => <option key={h.id} value={h.id}>{h.name}</option>)}
          </select>
          <input type="datetime-local" required value={sessionForm.start_time} onChange={(e) => setSessionForm({ ...sessionForm, start_time: e.target.value })} />
          <input placeholder="Price, ₽" type="number" min="1" step="any" required value={sessionForm.price}
            onChange={(e) => setSessionForm({ ...sessionForm, price: e.target.value })} />
          <button className="btn">Add session</button>
        </form>
      </div>

      <h2>Halls</h2>
      <table>
        <thead><tr><th>Name</th><th>Size</th><th>Status</th><th /></tr></thead>
        <tbody>
          {halls.map((h) => (
            <tr key={h.id}>
              <td>{h.name}</td>
              <td>{h.rows} × {h.seats_per_row}</td>
              <td>{h.is_active ? "Open" : "Closed"}</td>
              <td><button className="btn small ghost" onClick={() => toggleHall(h)}>{h.is_active ? "Close" : "Reopen"}</button></td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Sessions</h2>
      <table>
        <thead><tr><th>Time</th><th>Movie</th><th>Hall</th><th>Price</th><th /></tr></thead>
        <tbody>
          {sessions.map((s) => (
            <tr key={s.id}>
              <td>{formatTime(s.start_time)}</td>
              <td>{movieTitle(s.movie_id)}</td>
              <td>{hallName(s.hall_id)}</td>
              <td>{formatPrice(s.price)}</td>
              <td className="actions">
                <input className="price-input" type="number" min="1" placeholder="New price" value={prices[s.id] ?? ""}
                  onChange={(e) => setPrices({ ...prices, [s.id]: e.target.value })} />
                <button className="btn small ghost" disabled={!prices[s.id]} onClick={() => updatePrice(s.id)}>Set</button>
                <button className="btn small danger" onClick={() => deleteSession(s.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Bookings</h2>
      {bookings.length === 0 && <p className="muted">No bookings yet.</p>}
      {bookings.length > 0 && (
        <table>
          <thead><tr><th>Code</th><th>Customer</th><th>Movie</th><th>Time</th><th>Seats</th><th>Total</th></tr></thead>
          <tbody>
            {bookings.map((b) => (
              <tr key={b.id}>
                <td>#{b.booking_code}</td>
                <td>{b.customer_name}</td>
                <td>{b.movie_title}</td>
                <td>{formatTime(b.start_time)}</td>
                <td>{b.tickets.map((t) => `R${t.row}-${t.number}`).join(", ")}</td>
                <td>{formatPrice(b.total_price)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}
