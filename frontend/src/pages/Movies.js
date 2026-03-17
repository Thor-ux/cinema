import { useEffect, useState } from "react";
import { apiFetch } from "../api";
import { Link } from "react-router-dom";

export default function Movies() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    apiFetch("/movies")
    .then(res => setMovies(res.data))
    .catch(() => alert("Failed to load movies"));
  }, []);

  return (
    <div>
      <h2>Movies</h2>
      {movies.length === 0 && <p> No movies available.</p>}
      {movies.map((movie) => (
        <div key={movie.id}>
          <h3>{movie.title}</h3>
          <p>{movie.description}</p>
          <p>Duration: {movie.duration_minutes} mins</p>
          <Link to={`/movies/${movie.id}`}>
            View Showtimes
          </Link>
        </div>
      ))}
    </div>
  );
}
