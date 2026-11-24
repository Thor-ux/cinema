import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export default function Movies() {
  const [movies, setMovies] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/movies").then(setMovies).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (!movies) return <p className="muted">Loading movies…</p>;

  return (
    <>
      <h1>Now showing</h1>
      {movies.length === 0 && <p className="muted">No movies yet.</p>}
      <div className="grid">
        {movies.map((m) => (
          <Link key={m.id} to={`/movies/${m.id}`} className="card movie">
            <div className="poster">{m.title.slice(0, 1)}</div>
            <h3>{m.title}</h3>
            <p className="muted">{m.duration_minutes} min</p>
            {m.description && <p>{m.description}</p>}
            <span className="btn small">Showtimes →</span>
          </Link>
        ))}
      </div>
    </>
  );
}
