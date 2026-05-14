from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.user import User
from app.core.config import settings

security = HTTPBearer()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

def get_current_admin(
    user: User = Depends(get_current_user)
):

    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    return user