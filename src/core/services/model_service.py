from typing import List, Union
from fastapi import status

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.model.model import Model
from core.model.exception import DefaultExceptions, LogicException
from core.model.token import Token


def get_by_id(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    model_id: str,
    token: Token,
) -> Union[Model, LogicException]:
    """gets model by model id

    Args:
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        model_id (str) : model id
        token (Token) : authentication token

    Returns:
        model object

    Raises:
        unauthorized exception, if not authenticated
        not found exception, if model was not found in database
        unprocessable entity exception, if model id is not valid

    """
    try:
        if not authentication_port.validate_token(token):
            raise DefaultExceptions.credentials_exception

        model = database_port.get_model_by_id(model_id)

        if model is None:
            raise LogicException("model not found", status.HTTP_404_NOT_FOUND)

    except LogicException:
        raise
    except:
        raise LogicException(
            "model id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    return model


def get_list(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    token: Token,
) -> Union[List[Model], LogicException]:
    """gets model list

    Args:
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        token (Token): authentication token

    Returns:
        list of model objects

    Raises:
        unauthorized exception, if not authenticated
        internal server error exception, if list could not be retrieved

    """
    try:
        if not authentication_port.validate_token(token):
            raise DefaultExceptions.credentials_exception

        model_list = database_port.get_model_list()

    except LogicException:
        raise
    except:
        raise LogicException(
            "cound not retrieve model list", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return model_list
