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

  const [priceUpdates, setPriceUpdates] = useState({});

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
          movie_id: Number(form.movie_id),
          hall_id: Number(form.hall_id),
          start_time: form.start_time,
          price: Number(form.price)
        })
      });

      alert("Session created");

      setForm({
        movie_id: "",
        hall_id: "",
        start_time: "",
        price: ""
      });

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

  async function updatePrice(id) {
    const newPrice = priceUpdates[id];

    if (!newPrice) {
      alert("Enter a price");
      return;
    }

    try {
      await apiFetch(
        `/admin/sessions/${id}/price?price=${newPrice}`,
        {
          method: "PATCH"
        }
      );

      alert("Price updated");

      loadData();

    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Admin Dashboard</h1>

      {/* CREATE SESSION */}
      <h2>Create Session</h2>

      <form onSubmit={createSession}>
        <input
          placeholder="Movie ID"
          value={form.movie_id}
          onChange={(e) =>
            setForm({
              ...form,
              movie_id: e.target.value
            })
          }
        />

        <input
          placeholder="Hall ID"
          value={form.hall_id}
          onChange={(e) =>
            setForm({
              ...form,
              hall_id: e.target.value
            })
          }
        />

        <input
          type="datetime-local"
          value={form.start_time}
          onChange={(e) =>
            setForm({
              ...form,
              start_time: e.target.value
            })
          }
        />

        <input
          placeholder="Price"
          value={form.price}
          onChange={(e) =>
            setForm({
              ...form,
              price: e.target.value
            })
          }
        />

        <button type="submit">
          Create Session
        </button>
      </form>

      {/* SESSIONS */}
      <h2>Sessions</h2>

      {sessions.map((s) => (
        <div
          key={s.id}
          style={{
            border: "1px solid #ccc",
            marginBottom: "15px",
            padding: "10px"
          }}
        >
          <p>
            <strong>Movie:</strong> {s.movie_id}
          </p>

          <p>
            <strong>Hall:</strong> {s.hall_id}
          </p>

          <p>
            <strong>Start:</strong>{" "}
            {new Date(s.start_time).toLocaleString()}
          </p>

          <p>
            <strong>Price:</strong> ${s.price}
          </p>

          <input
            placeholder="New price"
            value={priceUpdates[s.id] || ""}
            onChange={(e) =>
              setPriceUpdates({
                ...priceUpdates,
                [s.id]: e.target.value
              })
            }
          />

          <button onClick={() => updatePrice(s.id)}>
            Update Price
          </button>

          <button
            onClick={() => deleteSession(s.id)}
            style={{ marginLeft: "10px" }}
          >
            Delete
          </button>
        </div>
      ))}

      {/* BOOKINGS */}
      <h2>Bookings</h2>

      {bookings.map((b, index) => (
        <div
          key={index}
          style={{
            border: "1px solid #ddd",
            marginBottom: "10px",
            padding: "10px"
          }}
        >
          <p>
            <strong>Booking:</strong> #{b.booking_id}
          </p>

          <p>
            <strong>Code:</strong> {b.booking_code}
          </p>

          <p>
            <strong>Customer:</strong> {b.customer_name}
          </p>

          <p>
            <strong>Movie:</strong> {b.movie_title}
          </p>

          <p>
            <strong>Session:</strong>{" "}
            {new Date(b.session_time).toLocaleString()}
          </p>

          <p>
            <strong>Seat:</strong> Row {b.seat_row} /
            Seat {b.seat_number}
          </p>

          <p>
            <strong>Type:</strong> {b.seat_type}
          </p>
        </div>
      ))}
    </div>
  );
}