from fastapi import status
from typing import Tuple

from core.model.exception import LogicException
from core.model.inference import Inference
from core.model.result import Result
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
