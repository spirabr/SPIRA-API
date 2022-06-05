from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
from typing import Union

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass(frozen=True)
class User(BaseModel):
    id: str
    username: str
    email: str


@dataclass_json(letter_case=LetterCase.SNAKE)
class UserForm(BaseModel):
    username: str
    email: str
    password: str


@dataclass_json(letter_case=LetterCase.SNAKE)
class AuthenticationUser(BaseModel):
    username: str
    email: str
    hashed_password: str
    id: Union[str, None] = None
