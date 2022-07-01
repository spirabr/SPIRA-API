from pydantic import BaseModel
from typing import Optional
from typing import Literal

sex_type = Literal["F", "M"]
mask_use_type = Literal["unmasked", "light", "heavy"]


class InferenceCreationForm(BaseModel):
    age: int
    sex: sex_type
    mask_use: mask_use_type
    SPO2: int
    BPM: int
    respiratory_frequency: int
    tested_positive_covid_before: Optional[bool]
    is_hospitalized: bool
    IDC: Optional[int]
    model_id: str


class InferenceCreation(InferenceCreationForm):
    status: str
    user_id: str


class UploadAudio(BaseModel):
    content: bytes
    filename: str


class InferenceFiles(BaseModel):
    vogal_sustentada: UploadAudio
    parlenda_ritmada: UploadAudio
    frase: UploadAudio


class Inference(InferenceCreation):
    id: str
