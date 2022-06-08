from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass(frozen=True)
class User(BaseModel):
    id: str
    username: str
    email: str


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass(frozen=True)
class UserForm(BaseModel):
    id: str
    username: str
    email: str
    password: str
