from typing import List, Union
from fastapi import status
from core.model.constants import Status
from core.model.message_service import RequestLetter
from core.model.token import Token
from core.ports.authentication_port import AuthenticationPort

from core.ports.database_port import DatabasePort
from core.model.inference import (
    Inference,
    InferenceCreation,
    InferenceCreationForm,
    InferenceFiles,
)
from core.model.exception import DefaultExceptions, LogicException
from core.ports.message_service_port import MessageServicePort
from core.ports.simple_storage_port import SimpleStoragePort

import core.services.model_service as model_service


def get_by_id(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    inference_id: str,
    user_id: str,
    token: Token,
) -> Union[Inference, LogicException]:

    try:
        _authenticate_user(authentication_port, database_port, user_id, token)
        inference = database_port.get_inference_by_id(inference_id, user_id)
        if inference is None:
            raise LogicException("inference not found", status.HTTP_404_NOT_FOUND)

    except LogicException:
        raise
    except:
        raise LogicException(
            "inference id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    return inference


def get_list(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_id: str,
    token: Token,
) -> Union[List[Inference], LogicException]:

    try:
        _authenticate_user(authentication_port, database_port, user_id, token)
        inference_list = database_port.get_inference_list(user_id)

    except LogicException:
        raise
    except:
        raise LogicException(
            "cound not retrieve inference list", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return inference_list


async def create_new_inference(
    simple_storage_port: SimpleStoragePort,
    message_service_port: MessageServicePort,
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_id: str,
    inference_form: InferenceCreationForm,
    inference_files: InferenceFiles,
    token: Token,
):
    try:
        _authenticate_user(authentication_port, database_port, user_id, token)
        _validate_new_inference(authentication_port, database_port, inference_form)

        new_inference = InferenceCreation(
            age=inference_form.age,
            sex=inference_form.sex,
            user_id=user_id,
            model_id=inference_form.model_id,
            status=Status.processing_status,
        )
        new_id = database_port.insert_inference(new_inference)

        model = model_service.get_by_id(
            authentication_port, database_port, inference_form.model_id, token
        )

        _store_files(simple_storage_port, inference_files, new_id)

        await message_service_port.send_message(
            RequestLetter(
                content=new_inference, publishing_channel=model.receiving_channel
            )
        )
    except LogicException:
        raise
    except:
        raise LogicException(
            "cound not create new inference", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return new_id


def _authenticate_user(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_id: str,
    token: Token,
):
    try:
        decoded_token_content = authentication_port.decode_token(token)
        user = database_port.get_user_by_username(decoded_token_content.username)
        if user.id != user_id:
            raise DefaultExceptions.forbidden_exception

    except LogicException:
        raise
    except:
        raise DefaultExceptions.credentials_exception


def _validate_new_inference(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    inference_form: InferenceCreationForm,
):
    try:
        model = database_port.get_model_by_id(inference_form.model_id)
        if model is None:
            raise LogicException("model not found", status.HTTP_404_NOT_FOUND)

    except LogicException:
        raise
    except:
        raise LogicException(
            "model id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )


def _store_files(
    simple_storage_port: SimpleStoragePort, files: InferenceFiles, inference_id: str
):
    try:
        file_types = InferenceFiles.__fields__.keys()
        for file_type in file_types:
            simple_storage_port.store_inference_file(
                inference_id, file_type, getattr(files, file_type)
            )

    except:
        raise LogicException(
            "could not store the audio files", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
