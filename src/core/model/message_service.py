from pydantic import BaseModel

from core.model.inference import Inference


class RequestLetter(BaseModel):
    content: Inference
    publishing_channel: str
