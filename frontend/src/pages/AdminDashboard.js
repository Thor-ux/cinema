import { useEffect, useState } from "react";
import { apiFetch } from "../api";

export default function AdminDashboard() {
  const [sessions, setSessions] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [form, setForm] = useState({
    movie_id: "",
    hall_id: "",
    start_time: "",
    price: ""
  });

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const sessionsData = await apiFetch("/admin/sessions");
      const bookingsData = await apiFetch("/admin/bookings");

      setSessions(sessionsData);
      setBookings(bookingsData);
    } catch (err) {
      alert(err.message);
    }
  }

  async function createSession(e) {
    e.preventDefault();

    try {
      await apiFetch("/admin/sessions", {
        method: "POST",
        body: JSON.stringify({
          ...form,
          movie_id: Number(form.movie_id),
          hall_id: Number(form.hall_id),
          price: Number(form.price)
        })
      });
      await apiFetch(`/admin/sessions/${id}/price`, {
        method: "PATCH",
        body: JSON.stringify({ price: newPrice })
      });

      alert("Session created");
      loadData();
    } catch (err) {
      alert(err.message);
    }
  }

  async function deleteSession(id) {
    if (!window.confirm("Delete session?")) return;

    try {
      await apiFetch(`/admin/sessions/${id}`, {
        method: "DELETE"
      });

      loadData();
    } catch (err) {
      alert(err.message);
    }
  }


  return (
    <div>
      <h1>Admin Dashboard</h1>

      {/* CREATE SESSION */}
      <h2>Create Session</h2>
      <form onSubmit={createSession}>
        <input
          placeholder="Movie ID"
          value={form.movie_id}
          onChange={e => setForm({ ...form, movie_id: e.target.value })}
        />
        <input
          placeholder="Hall ID"
          value={form.hall_id}
          onChange={e => setForm({ ...form, hall_id: e.target.value })}
        />
        <input
          type="datetime-local"
          value={form.start_time}
          onChange={e => setForm({ ...form, start_time: e.target.value })}
        />
        <input
          placeholder="Price"
          value={form.price}
          onChange={e => setForm({ ...form, price: e.target.value })}
        />
        <button type="submit">Create</button>
      </form>

      {/* SESSIONS */}
      <h2>Sessions</h2>
      {sessions.map(s => (
        <div key={s.id}>
          <p>
            Movie {s.movie_id} | Hall {s.hall_id} | {new Date(s.start_time).toLocaleString()}
          </p>
          <button onClick={() => deleteSession(s.id)}>Delete</button>
        </div>
      ))}

      {/* BOOKINGS */}
      <h2>Bookings</h2>
      {bookings.map(b => (
        <div key={b.id}>
          <p>
            Booking #{b.id} | Session {b.session_id} | {b.customer_name}
          </p>
        </div>
      ))}
    </div>
  );
}