# Cinema Booking
A full-stack web application for booking cinema tickets with:

Movie listings & showtimes

Seat selection & booking

QR code ticket generation

Admin interface for managing movies, halls, sessions, and prices

JWT authentication (users & admins)

PostgreSQL database backend

FastAPI backend & React frontend

Dockerized for easy deployment

## Prerequisites

Docker & Docker Compose installed

Node.js (for local frontend development)

Python 3.11+ (for local backend development)

# Build & Run

## Build and start all services:

docker compose up --build

## Access services:

Backend API: http://localhost:8000

Frontend: http://localhost:3000

API docs (OpenAPI): http://localhost:8000/docs

## To stop containers:

docker compose down

## To rebuild containers after changes:

docker compose up --build

# Backend Development (Local)

Activate virtual environment:

cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

### Install dependencies:

pip install -r requirements.txt

## Run server locally:

uvicorn app.main:app --reload

# Frontend Development (Local)
Install dependencies:

cd frontend
npm install

## Run React app:

npm start

# API Endpoints
### Public
GET /movies — List all movies
GET /movies/{id}/showtimes — Get showtimes for a movie
GET /sessions/{id}/seats — Get seats for a session

### User (JWT)
POST /register — Register user
POST /login — Login and get JWT token
POST /bookings — Book seats
GET /tickets/me — List user’s tickets

### Admin (JWT + Admin Role)
POST /admin/movies — Create movie
PUT /movies/{id} — Edit movie
DELETE /movies/{id} — Delete movie
POST /admin/sessions — Create session
PUT /admin/sessions/{id} — Edit session
DELETE /admin/sessions/{id} — Delete session
GET /admin/bookings — List all bookings

## Author
Built by Daniel with ☕ and patience