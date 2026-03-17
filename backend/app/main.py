from fastapi import FastAPI

from app.database import Base, engine
from app.models import booking, movie, hall, seat, session, ticket, user
from app.routers import movies, sessions, bookings, halls, admin, tickets, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cinema Booking API")

app.include_router(movies.router)
app.include_router(sessions.router)
app.include_router(bookings.router)
app.include_router(halls.router)
app.include_router(admin.router)
app.include_router(tickets.router)
app.include_router(auth.router)