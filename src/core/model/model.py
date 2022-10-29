from pydantic import BaseModel


class Model(BaseModel):
    name: str
    publishing_channel: str
    id: str


class ModelCreationForm(BaseModel):
    name: str
    publishing_channel: str
