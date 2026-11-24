import { BrowserRouter, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import Header from "./components/Header";
import AdminDashboard from "./pages/AdminDashboard";
import Login from "./pages/Login";
import Movies from "./pages/Movies";
import MyBookings from "./pages/MyBookings";
import Register from "./pages/Register";
import SeatSelection from "./pages/SeatSelection";
import Showtime from "./pages/Showtime";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Header />
        <main className="container">
          <Routes>
            <Route path="/" element={<Movies />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/movies/:movieId" element={<Showtime />} />
            <Route path="/sessions/:sessionId" element={<ProtectedRoute><SeatSelection /></ProtectedRoute>} />
            <Route path="/my-bookings" element={<ProtectedRoute><MyBookings /></ProtectedRoute>} />
            <Route path="/admin" element={<ProtectedRoute admin><AdminDashboard /></ProtectedRoute>} />
            <Route path="*" element={<p className="muted">Page not found.</p>} />
          </Routes>
        </main>
      </BrowserRouter>
    </AuthProvider>
  );
}
