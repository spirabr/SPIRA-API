from pydantic import BaseModel

from core.model.inference import InferenceCreation


class RequestLetter(BaseModel):
    content: InferenceCreation
    publishing_channel: str
