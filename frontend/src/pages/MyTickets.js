import { useEffect, useState } from "react";
import api from "../api/axios";

export default function MyTickets() {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    api.get("/tickets/me")
      .then(res => setTickets(res.data))
      .catch(() => alert("Failed to load tickets"));
  }, []);

  return (
    <div>
      <h2>My Tickets</h2>

      {tickets.length === 0 && <p>No tickets purchased yet.</p>}

      {tickets.map(ticket => (
        <div key={ticket.id} style={{ marginBottom: "20px" }}>
          <p><strong>Movie:</strong> {ticket.movie_title}</p>
          <p><strong>Seat:</strong> {ticket.seat_number}</p>
          <p><strong>Time:</strong> {new Date(ticket.start_time).toLocaleString()}</p>

          {ticket.qr_code && (
            <img
              src={`data:image/png;base64,${ticket.qr_code}`}
              alt="QR Code"
              width="150"
            />
          )}
        </div>
      ))}
    </div>
  );
}
