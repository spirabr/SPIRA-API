from pydantic import BaseModel
from typing import Optional
from typing import Literal

sex_type = Literal["F", "M"]


class InferenceCreationForm(BaseModel):
    rgh: str
    age: int
    sex: sex_type
    covid_status: str
    mask_type: Optional[str]
    model_id: str


class InferenceCreation(InferenceCreationForm):
    status: str
    user_id: str
    created_in: str


class UploadAudio(BaseModel):
    content: bytes
    filename: str


class InferenceFiles(BaseModel):
    aceite: UploadAudio
    vogal_sustentada: UploadAudio
    parlenda_ritmada: UploadAudio
    frase: UploadAudio


class Inference(InferenceCreation):
    id: str
