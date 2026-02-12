import { useEffect, useState } from "react";
import api from "../api/axios";

export default function MyBookings() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    api.get("/bookings/me").then(res => {
      setBookings(res.data);
    });
  }, []);

  return (
    <div>
      <h2>My Bookings</h2>
      {bookings.map(b => (
        <div key={b.id}>
          <p>Showtime: {b.showtime_id}</p>
          <img src={`data:image/png;base64,${b.qr_code}`} />
        </div>
      ))}
    </div>
  );
}
