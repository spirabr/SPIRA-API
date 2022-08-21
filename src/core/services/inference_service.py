from typing import List, Union
from fastapi import status
import datetime
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
    """gets inference by id from database

    Args:
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        inference_id (str) : inference id
        user_id (str) : user id
        token (Token): authentication token

    Returns:
        inference object

    Raises:
        unauthorized exception, if not authenticated
        forbidden exception, if token does not match user in request
        not found exception, if inference was not found in database
        unprocessable entity exception, if inference id is not valid

    """
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
    """gets inference list from database

    Args:
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        user_id (str) : user id
        token (Token): authentication token

    Returns:
        list of inference objects

    Raises:
        unauthorized exception, if not authenticated
        forbidden exception, if token does not match user in request
        internal server error exception, if list could not be retrieved

    """
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
) -> str:
    """creates new inference, inserts it in database,
     stores inference files in simple storage and sends inference message to message service

    Args:
        simple_storage_port (SimpleStoragePort) : simple storage port
        message_service_port (MessageServicePort): message service port
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        user_id (str) : user id
        inference_form (InferenceCreationForm) : new inference form
        inference_files (InferenceFiles) : inference request files
        token (Token): authentication token

    Returns:
        new inference id

    Raises:
        unauthorized exception, if not authenticated
        forbidden exception, if token does not match user in request
        internal server error exception, if inference could not be created

    """
    try:
        _authenticate_user(authentication_port, database_port, user_id, token)
        _validate_new_inference(database_port, inference_form)

        new_inference = InferenceCreation(
            age=inference_form.age,
            sex=inference_form.sex,
            user_id=user_id,
            rgh=inference_form.rgh,
            covid_status=inference_form.covid_status,
            mask_type=inference_form.mask_type,
            model_id=inference_form.model_id,
            status=Status.processing_status,
            created_in=str(datetime.datetime.now()),
        )
        new_id = database_port.insert_inference(new_inference)

        new_inserted_inference = Inference(
            id=new_id,
            age=inference_form.age,
            sex=inference_form.sex,
            user_id=user_id,
            rgh=inference_form.rgh,
            covid_status=inference_form.covid_status,
            mask_type=inference_form.mask_type,
            model_id=inference_form.model_id,
            status=Status.processing_status,
            created_in=str(datetime.datetime.now()),
        )

        model = model_service.get_by_id(
            authentication_port, database_port, inference_form.model_id, token
        )

        _store_files(simple_storage_port, inference_files, new_id)

        await message_service_port.send_message(
            RequestLetter(
                content=new_inserted_inference,
                publishing_channel=model.receiving_channel,
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
) -> None:
    """authenticates requesting user

    Args:
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        user_id (str) : user id
        token (Token): authentication token

    Returns:
        None

    Raises:
        unauthorized exception, if not authenticated
        forbidden exception, if token does not match user in request

    """
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
    database_port: DatabasePort,
    inference_form: InferenceCreationForm,
) -> None:
    """validates inference form data

    Args:
        database_port (DatabasePort) : database port
        inference_form (InferenceCreationForm) : inference creation form

    Returns:
        None

    Raises:
        model not found exception, if inference form model is not in database
        model id not valid exception, if inference form model id is not valid

    """
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
) -> None:
    """stores inference files in simple storage

    Args:
        simple_storage_port (SimpleStoragePort) : simple storage port
        inference_files (InferenceFiles) : inference request files
        inference_id (str) : inference id

    Returns:
        None

    Raises:
        internal server error exception, if inference could not be created

    """
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
