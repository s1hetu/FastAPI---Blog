import time
from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .models import Blog
from .schemas import BlogCreateSchema, BlogReadSchema, BlogReadSchemaWithUser
from src.auth.models import User
from ..auth.utils import get_current_user
from ..schema import Response

blog_router = APIRouter(prefix="/blog", tags=["Blog"])


@blog_router.get("/get_blog")
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    return db.query(Blog).filter(Blog.id == blog_id).first()


@blog_router.get("/get_all_blogs", response_model=list[BlogReadSchemaWithUser], tags=["All"])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).all()


@blog_router.post("/create_blog")
def create_blog(blog: BlogCreateSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    blog = Blog(title=blog.title, description=blog.description, user=user)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    response = Response(status_code=HTTPStatus.CREATED, message='Blog created successfully!')
    return response.success_response()


@blog_router.get("/my_blogs", response_model=list[BlogReadSchema])
def view_my_blogs(user: User = Depends(get_current_user)):
    return user.blogs


@blog_router.patch("/my_blogs/{blog_id}")
def update_blog(blog_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db), title: str = None, description: str = None):
    blog_obj = db.execute(
        select(Blog).where(Blog.id == blog_id)
    ).scalar()
    if not blog_obj:
        response = Response(status_code=404, message="Blog not found.")
        return response.error_response()
    if blog_obj.user != user:
        response = Response(status_code=404, message="Only blog owners can edit the blogs.")
        return response.error_response()
    if title or description:
        db.execute(
            update(Blog).where(Blog.id == blog_id).values(title=title, description=description)
        )
        response = Response(status_code=200, message="Blog Updated successfully")
        return response.success_response()
