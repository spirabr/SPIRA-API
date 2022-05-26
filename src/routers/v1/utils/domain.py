from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    id: Union[str, None] = None
    username: Union[str, None] = None
    email: Union[str, None] = None
