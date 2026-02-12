import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/axios";

export default function Showtime() {
  const { movieId } = useParams();
  const [showtimes, setShowtime] = useState([]);

  useEffect(() => {
    api
      .get(`/movies/${movieId}/showtime`)
      .then((res) => setShowtimes(res.data))
      .catch(() => alert("Failed to load showtimes"));
  }, [movieId]);

  return (
    <div>
      <h2>Showtimes</h2>

      {showtimes.length === 0 && <p>No showtimes available</p>}

      {showtimes.map((show) => (
        <div key={show.id}>
          <p>
            {new Date(show.start_time).toLocaleString()}
          </p>

          <Link to={`/seats/${show.id}`}>
            Select Seats
          </Link>
        </div>
      ))}
    </div>
  );
}
