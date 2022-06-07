from typing import Union

from domain.model.user import User, AuthenticationUser
from domain.model.model import Model


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


def model_helper(data) -> Union[Model, None]:
    if data == None:
        return None
    return Model(
        **{
            "id": str(data["_id"]),
            "name": data["name"],
            "subscribing_topic": data["subscribing_topic"],
            "publishing_topic": data["publishing_topic"],
        }
    )
