from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({
        "user_id": user.id,
        "is_admin": user.is_admin
    })

    return {"access_token": token}