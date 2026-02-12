import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";

export default function SeatSelection() {
  const { showtimeId } = useParams();
  const [seats, setSeats] = useState([]);
  const [selected, setSelected] = useState([]);

  useEffect(() => {
    api.get(`/showtimes/${showtimeId}/seats`)
      .then(res => setSeats(res.data));
  }, [showtimeId]);

  const toggleSeat = (seatId) => {
    setSelected(prev =>
      prev.includes(seatId)
        ? prev.filter(id => id !== seatId)
        : [...prev, seatId]
    );
  };

  const bookSeats = async () => {
    await api.post("/bookings", {
      showtime_id: showtimeId,
      seat_ids: selected
    });

    alert("Booking successful!");
  };

  return (
    <div>
      <h2>Select Seats</h2>
      <div>
        {seats.map(seat => (
          <button
            key={seat.id}
            disabled={seat.is_booked}
            onClick={() => toggleSeat(seat.id)}
          >
            {seat.number}
          </button>
        ))}
      </div>

      <button onClick={bookSeats}>
        Confirm Booking
      </button>
    </div>
  );
}
