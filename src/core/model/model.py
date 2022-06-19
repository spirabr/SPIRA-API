from pydantic import BaseModel


class Model(BaseModel):
    name: str
    receiving_channel: str
    publishing_channel: str
    id: str
