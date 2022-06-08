from typing import Union

from core.model.user import User


class DatabasePort:
    def __init__(self, database_adapter):
        self._database = database_adapter

    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        user = self._database.get_user_by_id(user_id)
        if user == None:
            return None
        return User(
            **{
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
            }
        )
