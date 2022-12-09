from pydantic import BaseModel


class Hospital(BaseModel):
    name: str
    id: str