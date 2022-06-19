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
    try:
        inference = inference_service.get_by_id(
            authentication_port, database_port, inference_id, user_id, token
        )
    except LogicException as e:
        raise e
    result = database_port.get_result_by_inference_id(inference_id)
    try:
        result = database_port.get_result_by_inference_id(inference_id)
    except:
        raise LogicException(
            "inference id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    if result is None:
        raise LogicException("result not found", status.HTTP_404_NOT_FOUND)
    return inference, result


def create_inference_result(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_id: str,
    inference_id: str,
    token: Token,
):
    try:
        decoded_token_content = authentication_port.decode_token(token)
        user = database_port.get_user_by_username(decoded_token_content.username)
    except:
        raise DefaultExceptions.credentials_exception

    if user.id != user_id:
        raise DefaultExceptions.forbidden_exception

    try:
        new_result = ResultCreation(
            inference_id=inference_id, output=-1, diagnosis="not available"
        )

    except:
        raise LogicException(
            "cound not create new inference result",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    database_port.insert_result(new_result)


def update_inference_result(database_port: DatabasePort, result_update: ResultUpdate):
    try:
        database_port.update_result(result_update)
    except:
        raise
