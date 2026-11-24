import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(form.email, form.password);
      navigate(location.state?.from || "/", { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="card form narrow" onSubmit={submit}>
      <h2>Log in</h2>
      {location.state?.registered && <p className="success">Account created. Please log in.</p>}
      <label>Email<input type="email" required autoComplete="email" value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
      <label>Password<input type="password" required autoComplete="current-password" value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
      {error && <p className="error">{error}</p>}
      <button className="btn" disabled={busy}>{busy ? "Logging in…" : "Log in"}</button>
      <p className="muted">No account? <Link to="/register">Sign up</Link></p>
    </form>
  );
}
