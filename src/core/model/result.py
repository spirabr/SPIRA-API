from typing import List
from pydantic import BaseModel


class Result(BaseModel):
    inference_id: str
    output: List[float]
    diagnosis: str
    id: str


class ResultCreation(BaseModel):
    inference_id: str
    output: List[float]
    diagnosis: str


class ResultUpdate(BaseModel):
    inference_id: str
    output: List[float]
    diagnosis: str
