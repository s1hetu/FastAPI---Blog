from datetime import datetime
from src.auth.schemas import UserNameSchema
from pydantic import BaseModel


class BlogCreateSchema(BaseModel):
    title: str
    description: str


class BlogReadSchema(BlogCreateSchema):
    date: datetime | None = None


class BlogReadSchemaWithUser(BlogReadSchema):

    date: datetime | None = None
    user: UserNameSchema

    class Config:
        from_attributes = True


