import { useEffect, useState } from "react";
import api from "../api/axios";
import { Link } from "react-router-dom";

export default function Movies() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    api.get("/movies").then((res) => {
      setMovies(res.data);
    });
  }, []);

  return (
    <div>
      <h2>Movies</h2>
      {movies.map((movie) => (
        <div key={movie.id}>
          <h3>{movie.title}</h3>
          <Link to={`/showtimes/${movie.id}`}>
            View Showtimes
          </Link>
        </div>
      ))}
    </div>
  );
}
