import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, formatPrice, formatTime } from "../api/client";
import Booking from "../components/Ticket";

const VIP_MULTIPLIER = 2;
const MAX_SEATS = 10;

export default function SeatSelection() {
  const { sessionId } = useParams();
  const [session, setSession] = useState(null);
  const [movie, setMovie] = useState(null);
  const [seats, setSeats] = useState([]);
  const [selected, setSelected] = useState([]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [booking, setBooking] = useState(null);

  const loadSeats = () => api(`/sessions/${sessionId}/seats`).then(setSeats);

  useEffect(() => {
    api(`/sessions/${sessionId}`)
      .then((s) => {
        setSession(s);
        return api(`/movies/${s.movie_id}`).then(setMovie);
      })
      .then(loadSeats)
      .catch((e) => setError(e.message));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionId]);

  const toggle = (seat) => {
    setError("");
    setSelected((cur) => {
      if (cur.includes(seat.id)) return cur.filter((id) => id !== seat.id);
      if (cur.length >= MAX_SEATS) {
        setError(`You can book up to ${MAX_SEATS} seats at once.`);
        return cur;
      }
      return [...cur, seat.id];
    });
  };

  const priceOf = (seat) => session.price * (seat.type === "vip" ? VIP_MULTIPLIER : 1);
  const chosen = seats.filter((s) => selected.includes(s.id));
  const total = chosen.reduce((sum, s) => sum + priceOf(s), 0);

  const book = async () => {
    setError("");
    setBusy(true);
    try {
      setBooking(await api("/bookings", {
        method: "POST",
        body: { session_id: Number(sessionId), seat_ids: selected, customer_name: name.trim() },
      }));
      setSelected([]);
    } catch (err) {
      setError(err.message);
      if (err.status === 409) loadSeats(); // someone else took a seat
    } finally {
      setBusy(false);
    }
  };

  if (booking) {
    return (
      <>
        <h1>You're booked! 🎟</h1>
        <p className="muted">Show these QR codes at the entrance. You can also find them under <Link to="/my-bookings">My tickets</Link>.</p>
        <Booking booking={booking} />
      </>
    );
  }
  if (!session || !movie) return error ? <p className="error">{error}</p> : <p className="muted">Loading seats…</p>;

  const rows = seats.reduce((acc, s) => ((acc[s.row] ||= []).push(s), acc), {});

  return (
    <>
      <Link to={`/movies/${movie.id}`} className="muted">← {movie.title}</Link>
      <h1>Choose your seats</h1>
      <p className="muted">{formatTime(session.start_time)} · Hall {session.hall_id} · from {formatPrice(session.price)}</p>

      <div className="hall">
        <div className="screen">SCREEN</div>
        {Object.entries(rows).map(([row, list]) => (
          <div key={row} className="row">
            <span className="row-label">{row}</span>
            {list.map((seat) => (
              <button
                key={seat.id}
                className={`seat ${seat.type} ${seat.is_reserved ? "taken" : ""} ${selected.includes(seat.id) ? "selected" : ""}`}
                disabled={seat.is_reserved}
                onClick={() => toggle(seat)}
                title={`Row ${seat.row}, seat ${seat.number}${seat.type === "vip" ? " (VIP)" : ""}${seat.is_reserved ? " – taken" : ""}`}
                aria-pressed={selected.includes(seat.id)}
              >
                {seat.number}
              </button>
            ))}
          </div>
        ))}
        <div className="legend">
          <span><i className="seat standard" /> Standard {formatPrice(session.price)}</span>
          <span><i className="seat vip" /> VIP {formatPrice(session.price * VIP_MULTIPLIER)}</span>
          <span><i className="seat selected" /> Selected</span>
          <span><i className="seat taken" /> Taken</span>
        </div>
      </div>

      <div className="card checkout">
        <div>
          {chosen.length === 0 ? (
            <span className="muted">Select seats on the map</span>
          ) : (
            <>
              <strong>{chosen.length} seat{chosen.length > 1 ? "s" : ""}</strong>
              <span className="muted"> · {chosen.map((s) => `R${s.row}-${s.number}`).join(", ")}</span>
              <div className="total">{formatPrice(total)}</div>
            </>
          )}
        </div>
        <input placeholder="Name on booking" value={name} maxLength={100} onChange={(e) => setName(e.target.value)} />
        <button className="btn" disabled={busy || chosen.length === 0 || !name.trim()} onClick={book}>
          {busy ? "Booking…" : "Book"}
        </button>
      </div>
      {error && <p className="error">{error}</p>}
    </>
  );
}
