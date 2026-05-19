import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { apiFetch } from "../api";

export default function Showtime() {

  const { movieId } = useParams();

  const [showtimes, setShowtimes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    async function loadShowtimes() {

      try {

        const data = await apiFetch(
          `/movies/${movieId}/showtimes`
        );

        setShowtimes(data);

      } catch (err) {

        console.error(err);
        alert("Failed to load showtimes");

      } finally {

        setLoading(false);

      }
    }

    loadShowtimes();

  }, [movieId]);

  if (loading) {
    return <p>Loading showtimes...</p>;
  }

  return (
    <div>

      <h2>Showtimes</h2>

      {showtimes.length === 0 && (
        <p>No showtimes available</p>
      )}

      {showtimes.map((showtime) => (

        <div
          key={showtime.id}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            marginBottom: "10px"
          }}
        >

          <p>
            <strong>Time:</strong>{" "}
            {new Date(showtime.start_time).toLocaleString()}
          </p>

          <p>
            <strong>Price:</strong> ${showtime.price}
          </p>

          <p>
            <strong>Hall:</strong> {showtime.hall_id}
          </p>

          <Link to={`/seats/${showtime.id}`}>
            Select Seats
          </Link>

        </div>
      ))}

    </div>
  );
}