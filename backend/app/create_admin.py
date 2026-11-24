"""Create an admin user, or promote an existing user to admin.

Usage:  python -m app.create_admin admin@example.com 'a-strong-password'
"""
import sys

from email_validator import EmailNotValidError, validate_email

from app import models  # noqa: F401
from app.core.security import hash_password
from app.database import Base, SessionLocal, engine
from app.models import User


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    password = sys.argv[2]
    try:
        # Same check the login endpoint uses, so the admin can actually log in.
        email = validate_email(sys.argv[1], check_deliverability=False).normalized.lower()
    except EmailNotValidError as e:
        sys.exit(f"Invalid email: {e}")
    if len(password) < 8:
        sys.exit("Password must be at least 8 characters.")

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_admin = True
            print(f"{email} is now an admin.")
        else:
            db.add(User(email=email, password=hash_password(password), is_admin=True))
            print(f"Admin {email} created.")
        db.commit()


if __name__ == "__main__":
    main()
