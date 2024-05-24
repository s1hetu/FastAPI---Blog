from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.param_functions import Form
from database import get_db
from .models import User
from .schemas import UserCreateSchema, UserReadSchema, TokenSchema, UserProfileSchema
from .utils import get_hashed_password, verify_password, create_token, get_current_user
from ..blog.schemas import BlogCreateSchema

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.get("/get_all_users", response_model=list[UserReadSchema], tags=["All"])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@auth_router.post("/create_user", response_model=UserReadSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(detail="User Email already registered", status_code=400)
    else:
        user_obj = User(email=user.email, password=get_hashed_password(user.password), username=user.username)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj


class AuthRequestForm(OAuth2PasswordRequestForm):

    def __init__(self, username: Annotated[str, Form()], password: Annotated[str, Form()]):
        super().__init__(username=username, password=password)


@auth_router.post("/login", response_model=TokenSchema)
def login(data: AuthRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = user.password
    if not verify_password(data.password, hashed_password):
        return HTTPException(status_code=400, detail="Incorrect password.")
    return {
        "access_token": create_token("access", user.username),
        "refresh_token": create_token("refresh", user.username)
    }


@auth_router.get("/profile", response_model=UserProfileSchema)
def view_profile(user: User = Depends(get_current_user)):
    return user
