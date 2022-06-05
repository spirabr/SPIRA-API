from typing import Union

from domain.model.user import User, AuthenticationUser


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
