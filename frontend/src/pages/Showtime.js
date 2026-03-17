import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { apiFetch } from "../api";

export default function Showtime() {
  const { movieId } = useParams();
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    apiFetch(`/sessions/${movieId}`)
      .then(setSessions(res.data))
      .catch(() => alert("Failed to load showtimes"));
  }, [movieId]);

  return (
    <div>
      <h2>Showtimes</h2>

      {sessions.length === 0 && <p>No showtimes available</p>}

      {sessions.map(session => (
        <div key={session.id}>
          <p>
            {new Date(show.start_time).toLocaleString()}
          </p>
          <p>${session.price}</p>

          <Link to={`/sessions/${session.id}`}>
            Select Seats
          </Link>
        </div>
      ))}
    </div>
  );
}
