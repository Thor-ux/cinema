import { formatPrice, formatTime } from "../api/client";

export default function Booking({ booking }) {
  return (
    <article className="card booking">
      <div className="booking-head">
        <div>
          <h3>{booking.movie_title}</h3>
          <p className="muted">{formatTime(booking.start_time)} · {booking.hall_name}</p>
        </div>
        <div className="right">
          <div className="code">#{booking.booking_code}</div>
          <div className="muted">{formatPrice(booking.total_price)}</div>
        </div>
      </div>
      <div className="tickets">
        {booking.tickets.map((t) => (
          <div key={t.id} className="ticket">
            <img src={`data:image/png;base64,${t.qr_code}`} alt={`QR code for row ${t.row}, seat ${t.number}`} />
            <div>Row {t.row}, seat {t.number}</div>
            <div className="muted">{t.seat_type === "vip" ? "VIP · " : ""}{formatPrice(t.price)}</div>
          </div>
        ))}
      </div>
    </article>
  );
}
