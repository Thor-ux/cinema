import { useEffect, useState } from "react";
import { apiFetch } from "../api";

export default function MyBookings() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    apiFetch("/bookings/me")
    .then(res => {setBookings(res.data)
    .catch(() => alert("Failed to load bookings"));
    });
  }, []);

  return (
    <div>
      <h2>My Bookings</h2>
      {bookings.map(b => (
        <div key={b.id}>
          <p>Showtime: {b.session_id}</p>
          <img src={`data:image/png;base64,${b.qr_code}`} />
        </div>
      ))}
    </div>
  );
}
