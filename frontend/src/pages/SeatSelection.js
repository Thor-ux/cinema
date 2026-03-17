import { useEffect, useState } from "react";
import { apiFetch } from "../api";
import { useParams } from "react-router-dom";

export default function SeatSelection() {
  const { sessionId } = useParams();

  const [seats, setSeats] = useState([]);
  const [selectedSeat, setSelectedSeat] = useState(null);

  useEffect(() => {
    apiFetch(`/sessions/${sessionId}/seats`)
      .then(setSeats)
      .catch(err => alert(err.message));
  }, [sessionId]);

  const handleBooking = async () => {
    if (!selectedSeat) {
      alert("Select a seat first");
      return;
    }

    try {
      await apiFetch("/bookings", {
        method: "POST",
        body: JSON.stringify({
          session_id: sessionId,
          seat_id: selectedSeat,
        }),
      });

      alert("Booking successful 🎟");
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div>
      <h2>Select Seat</h2>

      <div style={{ display: "flex", flexWrap: "wrap", maxWidth: "300px" }}>
        {seats.map(seat => (
          <button
            key={seat.id}
            disabled={seat.is_booked}
            onClick={() => setSelectedSeat(seat.id)}
            style={{
              margin: "5px",
              background:
                seat.id === selectedSeat
                  ? "green"
                  : seat.is_booked
                  ? "gray"
                  : "white",
            }}
          >
            {seat.number}
          </button>
        ))}
      </div>

      <button onClick={handleBooking} style={{ marginTop: "20px" }}>
        Book Seat
      </button>
    </div>
  );
}