from pydantic import BaseModel


class Result(BaseModel):
    status: str
    inference_id: str
    output: float
    diagnosis: str
    id: str


class ResultCreation(BaseModel):
    status: str
    inference_id: str
    output: float
    diagnosis: str
