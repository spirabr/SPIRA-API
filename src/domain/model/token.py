from dataclasses import dataclass
from pydantic import BaseModel

from dataclasses_json import dataclass_json, LetterCase
from typing import Union


@dataclass_json(letter_case=LetterCase.SNAKE)
class Token(BaseModel):
    access_token: str
    token_type: str


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass(frozen=True)
class TokenData(BaseModel):
    username: Union[str, None] = None


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass(frozen=True)
class JWTData(BaseModel):
    sub: Union[str, None] = None
