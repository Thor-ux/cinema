import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import Booking from "../components/Ticket";

export default function MyBookings() {
  const [bookings, setBookings] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/bookings/me").then(setBookings).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (!bookings) return <p className="muted">Loading…</p>;

  return (
    <>
      <h1>My tickets</h1>
      {bookings.length === 0 && <p className="muted">No bookings yet. <Link to="/">Find a movie</Link></p>}
      {bookings.map((b) => <Booking key={b.id} booking={b} />)}
    </>
  );
}
