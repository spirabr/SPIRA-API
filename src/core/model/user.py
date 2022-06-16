from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    email: str


class UserWithPassword(User):
    password: str


class UserCreation(BaseModel):
    username: str
    email: str
    password: str


class UserCreationForm(UserCreation):
    password_confirmation: str
