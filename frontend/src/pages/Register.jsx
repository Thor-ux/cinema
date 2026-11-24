import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api/client";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await api("/auth/register", { method: "POST", body: form });
      navigate("/login", { state: { registered: true } });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="card form narrow" onSubmit={submit}>
      <h2>Create an account</h2>
      <label>Email<input type="email" required autoComplete="email" value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
      <label>Password <span className="muted">(at least 8 characters)</span>
        <input type="password" required minLength={8} maxLength={72} autoComplete="new-password" value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
      {error && <p className="error">{error}</p>}
      <button className="btn" disabled={busy}>{busy ? "Creating…" : "Sign up"}</button>
      <p className="muted">Already registered? <Link to="/login">Log in</Link></p>
    </form>
  );
}
