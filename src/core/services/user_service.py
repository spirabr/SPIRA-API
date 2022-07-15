from typing import Optional, Union
from fastapi import status
import re

from core.ports.authentication_port import AuthenticationPort
from core.ports.database_port import DatabasePort
from core.model.user import User, UserCreation, UserCreationForm, UserWithPassword
from core.model.exception import DefaultExceptions, LogicException
from core.model.token import Token, TokenData


def get_by_id(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_id: str,
    token: Token,
) -> Union[User, LogicException]:
    try:
        if not authentication_port.validate_token(token):
            raise DefaultExceptions.credentials_exception

        user = database_port.get_user_by_id(user_id)

        if user is None:
            raise LogicException("user not found", status.HTTP_404_NOT_FOUND)

    except LogicException:
        raise
    except:
        raise LogicException(
            "user id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    return user


def authenticate_and_generate_token(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    username: str,
    password: str,
) -> Token:
    try:
        user: User = _authenticate_user(
            authentication_port, database_port, username, password
        )
        if user is None:
            raise

        token = authentication_port.generate_token(
            data=TokenData(username=user.username)
        )
    except:
        raise DefaultExceptions.user_form_exception

    return token


def create_new_user(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_form: UserCreationForm,
    token: Token,
):

    try:
        if not authentication_port.validate_token(token):
            raise DefaultExceptions.credentials_exception

        _validate_new_user(database_port, user_form)

        new_user = UserCreation(
            username=user_form.username,
            email=user_form.email,
            password=user_form.password,
        )
        new_user.password = authentication_port.get_password_hash(new_user.password)
        database_port.insert_user(new_user)

    except LogicException:
        raise
    except:
        raise LogicException(
            "cound not create new user", status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _validate_new_user(
    database_port: DatabasePort,
    user_form: UserCreationForm,
):
    if user_form.password != user_form.password_confirmation:
        raise LogicException(
            "password and password confirmation don't match",
            status.HTTP_400_BAD_REQUEST,
        )
    existent_user = database_port.get_user_by_username(user_form.username)
    if existent_user is not None:
        raise LogicException(
            "username is already registered",
            status.HTTP_400_BAD_REQUEST,
        )
    existent_user = database_port.get_user_by_email(user_form.email)
    if existent_user is not None:
        raise LogicException(
            "email is already registered",
            status.HTTP_400_BAD_REQUEST,
        )
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_form.email):
        raise LogicException(
            "email format is invalid",
            status.HTTP_400_BAD_REQUEST,
        )


def _authenticate_user(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    username: str,
    plain_password: str,
) -> Optional[User]:
    user_with_password = database_port.get_user_by_username_with_password(username)
    if user_with_password is None or not authentication_port.verify_password(
        plain_password, user_with_password.password
    ):
        raise

    user: User = User(
        id=user_with_password.id,
        username=user_with_password.username,
        email=user_with_password.email,
    )
    return user
