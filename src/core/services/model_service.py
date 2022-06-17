from typing import List, Union
from fastapi import status

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.model.model import Model
from core.model.exception import LogicException
from core.model.token import Token


def get_by_id(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    model_id: str,
    token: Token,
) -> Union[Model, LogicException]:
    if not authentication_port.validate_token(token):
        raise LogicException(
            "could not validate the credentials", status.HTTP_401_UNAUTHORIZED
        )
    try:
        model = database_port.get_model_by_id(model_id)
    except:
        raise LogicException(
            "model id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    if model is None:
        raise LogicException("model not found", status.HTTP_404_NOT_FOUND)
    return model


def get_list(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    token: Token,
) -> Union[List[Model], LogicException]:
    if not authentication_port.validate_token(token):
        raise LogicException(
            "could not validate the credentials", status.HTTP_401_UNAUTHORIZED
        )
    try:
        model_list = database_port.get_model_list()
    except:
        raise LogicException(
            "cound not retrieve model list", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return model_list