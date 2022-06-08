from distutils.log import Log
from typing import Union
from fastapi import status

from core.ports.database_port import DatabasePort
from core.model.user import User
from core.model.exception import LogicException


def get_user_by_id_command(
    database_port: DatabasePort, user_id: str
) -> Union[User, LogicException]:
    try:
        user = database_port.get_user_by_id(user_id)
    except:
        return LogicException(
            "user id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    if user is None:
        return LogicException("user not found", status.HTTP_404_NOT_FOUND)
    return user
