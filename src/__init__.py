from fastapi import FastAPI
from src.blog.router import blog_router
from src.auth.router import auth_router


def create_app():
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(blog_router)

    return app
