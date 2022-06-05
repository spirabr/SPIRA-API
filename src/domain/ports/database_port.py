import inject
from typing import Union

from domain.model.user import User, UserForm
from domain.interfaces.database_interface import DatabaseInterface


class DatabasePort:
    @inject.autoparams()
    def __init__(self, database: DatabaseInterface):
        self._database = database

    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        return self._database.get_user_by_id(user_id)

    def get_user_by_username(self, username: str) -> Union[User, None]:
        return self._database.get_user_by_username(username)
