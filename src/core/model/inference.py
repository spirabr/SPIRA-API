from pydantic import BaseModel
from typing import Optional


class InferenceCreationForm(BaseModel):
    model_id: str
    rgh: str
    mask_type: str
    gender: str
    covid_status: str
    age: Optional[int]
    cid: Optional[str]
    bpm: Optional[str]
    respiratory_frequency: Optional[str]
    respiratory_insufficiency_status: Optional[str]
    location: Optional[str]
    last_positive_diagnose_date: Optional[str]
    hospitalized: Optional[str]
    hospitalization_start: Optional[str]
    hospitalization_end: Optional[str]
    spo2: Optional[str]


class InferenceCreation(InferenceCreationForm):
    status: str
    user_id: str
    created_in: str


class UploadAudio(BaseModel):
    content: bytes
    filename: str


class InferenceFiles(BaseModel):
    aceite: UploadAudio
    sustentada: UploadAudio
    parlenda: UploadAudio
    frase: Optional[UploadAudio]


class Inference(InferenceCreation):
    id: str
