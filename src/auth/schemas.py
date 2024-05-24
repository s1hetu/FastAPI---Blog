from pydantic import BaseModel


class UserNameSchema(BaseModel):
    username: str


class UserReadSchema(UserNameSchema):
    email: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserCreateSchema(UserReadSchema):
    password: str


class UserProfileSchema(UserReadSchema):
    is_active: bool
    # blogs: list["BlogReadSchema"]

