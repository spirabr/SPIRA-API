from pydantic import BaseModel


class Token(BaseModel):
    content: str


class TokenData(BaseModel):
    username: str
