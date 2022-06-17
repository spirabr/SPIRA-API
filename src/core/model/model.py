from pydantic import BaseModel


class Model(BaseModel):
    name: str
    subscribing_topic: str
    publishing_topic: str
    id: str
