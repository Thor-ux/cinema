# 🎬 Cinema Backend API

A Django REST Framework–based backend for a cinema booking system. This project handles movies, sessions, halls, seats, bookings, and authentication, with a clean API-first design.

---

## 🚀 Features

* Movies API (DRF)
* Seat availability & locking logic
* Auth-protected bookings
* Admin dashboard
* PostgreSQL database
---

## 🧱 Tech Stack

* Python 3.10+
* Django 5.x
* Django REST Framework
* PostgreSQL

---

## 📁 Project Structure

```
backend/
├── cinema/          # Project settings & root URLs
├── movies/          # Movies app
├── halls/           # Cinema halls & seats
├── bookings/        # Ticket bookings
├── users/           # Custom user model
├── manage.py
└── requirements.txt
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Thor-ux/Cinema-Backend-API.git
cd cinema-backend/backend
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## ▶️ Run the Server

```bash
python manage.py runserver
```

Visit:

* API: [http://USEIPOR.mydomain.com/](http://USEIPOR.mydomain.com/)
* Admin: [http://USEIPOR.mydomain.com/admin/](http://USEIPOR.mydomain.com/admin/)

---

## 🔐 Authentication

* Uses Django authentication
* Bookings endpoints are protected
* Admin access via `/admin/`

---

## 🧪 Roadmap

* WebSocket seat updates
* Payment simulation
* Seat types (VIP / Regular)
* QR code ticket validation
* Analytics dashboard

---

## 📝 License

MIT License

---

## 👤 Author

Built by Daniel with ☕ and patience.