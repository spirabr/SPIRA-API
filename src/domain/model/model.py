from pydantic import BaseModel
from typing import Union

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
class Model(BaseModel):
    name: str
    subscribing_topic: str
    publishing_topic: str
    id: Union[str, None] = None
