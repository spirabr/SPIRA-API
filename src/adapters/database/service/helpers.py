from typing import Union

from domain.model.user import User, AuthenticationUser
from domain.model.inference import Inference


def user_helper(data) -> Union[User, None]:
    if data == None:
        return None
    return User(
        **{
            "id": str(data["_id"]),
            "username": data["username"],
            "email": data["email"],
        }
    )


def auth_user_helper(data) -> Union[AuthenticationUser, None]:
    if data == None:
        return None
    return AuthenticationUser(
        **{
            "id": str(data["_id"]),
            "username": data["username"],
            "email": data["email"],
            "hashed_password": data["hashed_password"],
        }
    )


def inference_helper(data) -> Union[Inference, None]:
    if data == None:
        return None
    return Inference(
        **{
            "id": str(data["_id"]),
            "age": data["age"],
            "sex": data["sex"],
            "user_id": data["user_id"],
        }
    )
