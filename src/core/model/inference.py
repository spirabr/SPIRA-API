from pydantic import BaseModel


class Inference(BaseModel):
    id: str
    age: int
    sex: str
    user_id: str
    model_id: str
    status: str


class InferenceCreation(BaseModel):
    age: int
    sex: str
    user_id: str
    model_id: str
