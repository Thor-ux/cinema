import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();
  return (
    <header className="header">
      <Link to="/" className="logo">🎬 Cinema</Link>
      <nav>
        <NavLink to="/" end>Movies</NavLink>
        {user && <NavLink to="/my-bookings">My tickets</NavLink>}
        {user?.is_admin && <NavLink to="/admin">Admin</NavLink>}
        {user ? (
          <button className="link" onClick={logout}>Log out</button>
        ) : (
          <>
            <NavLink to="/login">Log in</NavLink>
            <NavLink to="/register" className="btn small">Sign up</NavLink>
          </>
        )}
      </nav>
    </header>
  );
}
