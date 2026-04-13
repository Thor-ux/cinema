from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies import get_db
from app.schemas.user import UserCreate, UserRead, LoginRequest
from app.core.security import verify_password, create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(UserRead).filter(UserRead.email == data.email).first()

    if not user or not verify_password(data.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({
        "user_id": user.id,
        "is_admin": user.is_admin
    })

    return {"access_token": token}

@router.post("/register", response_model=UserRead)
def register(data: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(UserCreate).filter(UserCreate.email == data.email).first()

    if existing:
        raise HTTPException(400, "Email already registered")
    
    user = UserRead(
        email=data.email,
        password=verify_password(data.password),
        is_admin=False
    )

    db.add(user)