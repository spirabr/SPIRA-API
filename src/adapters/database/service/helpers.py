from typing import Union

from domain.model.user import User


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
