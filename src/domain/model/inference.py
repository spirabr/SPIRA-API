from pydantic import BaseModel
from typing import Union

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
class Inference(BaseModel):
    id: Union[str, None] = None
    age: int
    sex: str
    user_id: str


@dataclass_json(letter_case=LetterCase.SNAKE)
class InferenceForm(BaseModel):
    id: Union[str, None] = None
    age: int
    sex: str
