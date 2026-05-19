import { useEffect, useState } from "react";
import { apiFetch } from "../api";
import { useParams } from "react-router-dom";

export default function SeatSelection() {

  const { sessionId } = useParams();

  const [seats, setSeats] = useState([]);
  const [selectedSeat, setSelectedSeat] = useState(null);
  const [customerName, setCustomerName] = useState("");

  useEffect(() => {

    async function loadSeats() {

      try {

        const data = await apiFetch(
          `/sessions/${sessionId}/seats`
        );

        setSeats(data);

      } catch (err) {

        alert(err.message);

      }
    }

    loadSeats();

  }, [sessionId]);

  async function handleBooking() {

    if (!selectedSeat) {
      alert("Select a seat first");
      return;
    }

    if (!customerName.trim()) {
      alert("Enter your name");
      return;
    }

    try {

      await apiFetch("/bookings", {
        method: "POST",

        body: JSON.stringify({
          session_id: Number(sessionId),
          customer_name: customerName,
          seat_ids: [selectedSeat]
        }),
      });

      alert("Booking successful 🎟");

      const updatedSeats = seats.map((seat) => {

        if (seat.id === selectedSeat) {
          return {
            ...seat,
            is_reserved: true
          };
        }

        return seat;
      });

      setSeats(updatedSeats);
      setSelectedSeat(null);

    } catch (err) {

      alert(err.message);

    }
  }

  return (
    <div>

      <h2>Select Seat</h2>

      <input
        type="text"
        placeholder="Name"
        value={customerName}
        onChange={(e) => setCustomerName(e.target.value)}
        style={{
          marginBottom: "20px",
          padding: "10px",
          width: "250px"
        }}
      />

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          maxWidth: "500px"
        }}
      >

        {seats.map((seat) => (

          <button
            key={seat.id}

            disabled={seat.is_reserved}

            onClick={() => setSelectedSeat(seat.id)}

            style={{
              width: "60px",
              height: "60px",
              margin: "5px",
              cursor: seat.is_reserved
                ? "not-allowed"
                : "pointer",

              background:
                seat.id === selectedSeat
                  ? "green"
                  : seat.is_reserved
                  ? "gray"
                  : seat.type === "vip"
                  ? "gold"
                  : "white",

              border: "1px solid black"
            }}
          >

            R{seat.row}
            <br />
            S{seat.number}

          </button>
        ))}

      </div>

      <button
        onClick={handleBooking}
        style={{
          marginTop: "20px",
          padding: "10px 20px"
        }}
      >
        Book Seat
      </button>

    </div>
  );
}