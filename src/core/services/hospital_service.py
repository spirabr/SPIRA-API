from typing import List, Union
from fastapi import status

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.model.model import Model, ModelCreationForm
from core.model.exception import DefaultExceptions, LogicException
from core.model.token import Token



def get_list(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    token: Token,
) -> Union[List[Model], LogicException]:
    """gets hospital list from database

    Args:
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        token (Token): authentication token

    Returns:
        list of hospital objects

    Raises:
        unauthorized exception, if not authenticated
        internal server error exception, if list could not be retrieved

    """
    try:
        if not authentication_port.validate_token(token):
            raise DefaultExceptions.credentials_exception

        hospital_list = database_port.get_hospital_list()

    except LogicException:
        raise
    except Exception as e:
        print(e, flush=True)
        raise LogicException(
            "cound not retrieve hospital list", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return hospital_list
