from pydantic import BaseModel
from typing import Union

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
class Result(BaseModel):
    status: str
    inference_id: str
    output: float
    diagnosis: str
    id: Union[str, None] = None
