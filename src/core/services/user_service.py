from typing import Optional, Union
from fastapi import status
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
    if not authentication_port.validate_token(token):
        raise DefaultExceptions.credentials_exception
    try:
        user = database_port.get_user_by_id(user_id)
    except:
        raise LogicException(
            "user id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    if user is None:
        raise LogicException("user not found", status.HTTP_404_NOT_FOUND)
    return user


def _authenticate_user(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    username: str,
    plain_password: str,
) -> Optional[User]:
    user_with_password: UserWithPassword = (
        database_port.get_user_by_username_with_password(username)
    )
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
    except:
        raise DefaultExceptions.user_form_exception
    token = authentication_port.generate_token(data=TokenData(username=user.username))
    return token


def _validate_new_user(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_form: UserCreationForm,
):
    if user_form.password != user_form.password_confirmation:
        raise LogicException(
            "password and password confirmation don't match",
            status.HTTP_400_BAD_REQUEST,
        )


def create_new_user(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_form: UserCreationForm,
    token: Token,
):
    if not authentication_port.validate_token(token):
        raise DefaultExceptions.credentials_exception
    try:
        _validate_new_user(authentication_port, database_port, user_form)
    except LogicException as e:
        raise e
    try:
        new_user = UserCreation(
            username=user_form.username,
            email=user_form.email,
            password=user_form.password,
        )
        new_user.password = authentication_port.get_password_hash(new_user.password)
        database_port.insert_user(new_user)
    except:
        raise LogicException(
            "cound not create new user", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
