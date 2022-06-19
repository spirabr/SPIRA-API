from pydantic import BaseModel


class Result(BaseModel):
    inference_id: str
    output: float
    diagnosis: str
    id: str


class ResultCreation(BaseModel):
    inference_id: str
    output: float
    diagnosis: str
