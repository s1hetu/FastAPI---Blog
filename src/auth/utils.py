from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

from database import get_db
from .models import User
from .schemas import UserReadSchema

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 100
ALGORITHM = "HS256"
JWT_SECRET_KEY = "wfhwe"
JWT_REFRESH_SECRET_KEY = "dscdshs"

auth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scheme_name="JWT")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_token(token_type: str, subject: str | None = None, expire_time: int | None = None) -> str:
    if token_type == "access":
        default_token_expiry_time = ACCESS_TOKEN_EXPIRE_MINUTES
        jwt_key = JWT_SECRET_KEY
    else:
        default_token_expiry_time = REFRESH_TOKEN_EXPIRE_MINUTES
        jwt_key = JWT_REFRESH_SECRET_KEY
    if expire_time:
        expire_time = datetime.utcnow() + timedelta(minutes=int(expire_time))
    else:
        expire_time = datetime.utcnow() + timedelta(minutes=int(default_token_expiry_time))
    to_encode = {"exp": expire_time, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, jwt_key, ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(auth2_scheme), db: Session = Depends(get_db)) -> UserReadSchema:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        expiry_time = payload.get('exp')
        if datetime.fromtimestamp(expiry_time) < datetime.now():
            raise HTTPException(status_code=401, detail="Token expired.", headers={"WWW-Authenticate": "Bearer"})
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"}, )
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
