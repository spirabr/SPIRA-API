from fastapi import status
from typing import Tuple

from core.model.exception import DefaultExceptions, LogicException
from core.model.inference import Inference
from core.model.result import Result, ResultCreation, ResultUpdate
from core.model.token import Token
from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
import core.services.inference_service as inference_service


def get_inference_result(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    inference_id: str,
    user_id: str,
    token: Token,
) -> Tuple[Inference, Result]:
    """gets the result object of an inference from database

    Args:
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        inference_id (str) : inference id
        user_id (str) : user id
        token (Token): authentication token

    Returns:
        A tuple where the first element is the inference whose id is given as
        an argument and the correspondent inference result object

    Raises:
        unauthorized exception, if not authenticated
        forbidden exception, if token does not match user in request
        not found exception, if inference was not found in database
        unprocessable entity exception, if inference id is not valid
        not found exception, if result was not found in database

    """
    try:
        inference = inference_service.get_by_id(
            authentication_port, database_port, inference_id, user_id, token
        )

        result = database_port.get_result_by_inference_id(inference_id)
        if result is None:
            raise LogicException("result not found", status.HTTP_404_NOT_FOUND)

    except LogicException:
        raise

    return inference, result


def create_inference_result(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_id: str,
    inference_id: str,
    token: Token,
) -> None:
    """creates the result object of an inference and inserts it in database

    Args:
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        user_id (str) : user id
        inference_id (str) : inference id
        token (Token): authentication token

    Returns:
        None

    Raises:
        unauthorized exception, if not authenticated
        forbidden exception, if token does not match user in request
        internal server exception, if there was an error creating result object

    """
    try:
        inference_service._authenticate_user(
            authentication_port, database_port, user_id, token
        )

        new_result = ResultCreation(
            inference_id=inference_id, output=-1, diagnosis="not available"
        )
        database_port.insert_result(new_result)

    except LogicException:
        raise
    except:
        raise LogicException(
            "cound not create new inference result",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def update_inference_result(
    database_port: DatabasePort, result_update: ResultUpdate
) -> None:
    """updates the result object in database

    Args:
        database_port (DatabasePort) : database port
        result_update (ResultUpdate) : result update form

    Returns:
        None

    Raises:
        internal server exception, if there was an error updating result object

    """
    try:
        database_port.update_result(result_update)
    except:
        raise LogicException(
            "cound not create new inference result",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
