import inject
from typing import Union

from domain.model.user import User, UserForm
from domain.ports.database_interface import DatabaseInterface


class UserActions:
    @inject.autoparams()
    def __init__(self, database: DatabaseInterface):
        self._database = database

    def execute_get_by_id(self, user_id: str) -> Union[User, None]:
        return self._database.get_user_by_id(user_id)
