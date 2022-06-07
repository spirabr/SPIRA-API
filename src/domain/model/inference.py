from dataclasses import dataclass
from pydantic import BaseModel

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
class Inference(BaseModel):
    id: str
    age: int
    sex: str
    user_id: str
