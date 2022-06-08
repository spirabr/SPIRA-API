from typing import Union

from domain.model.user import User, UserForm
from domain.interfaces.database_interface import DatabaseInterface


class DatabasePort:
    def __init__(self, adapter: DatabaseInterface):
        self._database = adapter

    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        return self._database.get_user_by_id(user_id)
