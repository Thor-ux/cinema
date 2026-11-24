import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, formatPrice } from "../api/client";

const dayLabel = (iso) => new Date(iso).toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long" });
const timeLabel = (iso) => new Date(iso).toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });

export default function Showtime() {
  const { movieId } = useParams();
  const [movie, setMovie] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([api(`/movies/${movieId}`), api(`/movies/${movieId}/showtimes`)])
      .then(([m, s]) => {
        setMovie(m);
        setSessions(s.filter((x) => new Date(x.start_time) > new Date()));
      })
      .catch((e) => setError(e.message));
  }, [movieId]);

  if (error) return <p className="error">{error}</p>;
  if (!movie) return <p className="muted">Loading…</p>;

  const byDay = Object.groupBy
    ? Object.groupBy(sessions, (s) => dayLabel(s.start_time))
    : sessions.reduce((acc, s) => ((acc[dayLabel(s.start_time)] ||= []).push(s), acc), {});

  return (
    <>
      <Link to="/" className="muted">← All movies</Link>
      <h1>{movie.title}</h1>
      <p className="muted">{movie.duration_minutes} min</p>
      {movie.description && <p>{movie.description}</p>}
      <h2>Showtimes</h2>
      {sessions.length === 0 && <p className="muted">No upcoming showtimes.</p>}
      {Object.entries(byDay).map(([day, list]) => (
        <section key={day} className="day">
          <h3>{day}</h3>
          <div className="times">
            {list.map((s) => (
              <Link key={s.id} to={`/sessions/${s.id}`} className="time">
                <strong>{timeLabel(s.start_time)}</strong>
                <span className="muted">Hall {s.hall_id} · {formatPrice(s.price)}</span>
              </Link>
            ))}
          </div>
        </section>
      ))}
    </>
  );
}
