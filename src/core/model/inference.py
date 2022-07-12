from typing import Any
from pydantic import BaseModel


class Inference(BaseModel):
    id: str
    age: int
    sex: str
    user_id: str
    model_id: str
    status: str


class InferenceCreationForm(BaseModel):
    age: int
    sex: str
    model_id: str


class InferenceCreation(InferenceCreationForm):
    status: str
    user_id: str


class InferenceFiles(BaseModel):
    vogal_sustentada: Any
    parlenda_ritmada: Any
    frase: Any
