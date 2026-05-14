from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.user import (
    UserCreate,
    UserRead,
    LoginRequest
)

from app.models.user import User

from app.core.security import (
    verify_password,
    hash_password,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead)
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=data.email,
        password=hash_password(data.password),
        is_admin=False
    )

    db.add(user)

    db.commit()
    db.refresh(user)

    return user


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "user_id": user.id,
        "is_admin": user.is_admin
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }