from typing import List, Union
from fastapi import status

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.model.model import Model, ModelCreationForm
from core.model.exception import DefaultExceptions, LogicException
from core.model.token import Token


def get_by_id(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    model_id: str,
    token: Token,
) -> Union[Model, LogicException]:
    """gets model by model id from database

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
    """gets model list from database

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


def create_new_model(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    model_form: ModelCreationForm,
    token: Token,
) -> None:
    """creates new model and inserts it in database

    Args:
        authentication_port (AuthenticationPort) : authentication port
        database_port (DatabasePort) : database port
        model_form (ModelCreationForm) : model creation form
        token (Token) : authentication token

    Returns:
        None

    Raises:
        unauthorized exception, if not authenticated
        invalid model form exception, if so
        internal server error exception, if the server was unable to create the model

    """
    try:
        if not authentication_port.validate_token(token):
            raise DefaultExceptions.credentials_exception

        _validate_new_model(database_port, model_form)

        new_model = ModelCreationForm(
            name=model_form.name, publishing_channel=model_form.publishing_channel
        )
        database_port.insert_model(new_model)

    except LogicException:
        raise
    except:
        raise LogicException(
            "cound not create new user", status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _validate_new_model(
    database_port: DatabasePort,
    model_form: ModelCreationForm,
):
    """validates the new model

    Args:
        database_port (DatabasePort) : database port
        model_form (ModelCreationForm) : model creation form

    Returns:
        None

    Raises:
        bad request exception, if name already exists
        bad request exception, if publishing channel already exists
    """

    existent_model = database_port.get_model_by_attribute(model_form.name, "name")
    if existent_model is not None:
        raise LogicException(
            "model name is already registered",
            status.HTTP_400_BAD_REQUEST,
        )
    existent_model = database_port.get_model_by_attribute(
        model_form.publishing_channel, "publishing_channel"
    )
    if existent_model is not None:
        raise LogicException(
            "publishing channel is already registered",
            status.HTTP_400_BAD_REQUEST,
        )
