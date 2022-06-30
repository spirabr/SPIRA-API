import pytest
from unittest.mock import MagicMock, patch
from fastapi import status


from core.model.exception import LogicException
from core.model.user import User, UserCreationForm
from core.ports.database_port import DatabasePort

from core.services.user_service import _validate_new_user
from tests.mocks.mongo_mock import MongoMock


@pytest.fixture()
def database_port():
    port = DatabasePort(MongoMock())
    return port


def test_user_validation_success_1(database_port: DatabasePort):
    def fake_get_user_by_username(username):
        return None

    user_form = UserCreationForm(
        **{
            "username": "test_username",
            "email": "valid@gmail.com",
            "password": "123abcde_?()",
            "password_confirmation": "123abcde_?()",
        }
    )

    with patch.object(
        database_port,
        "get_user_by_username",
        MagicMock(side_effect=fake_get_user_by_username),
    ) as mock_get_user_by_username:

        try:
            _validate_new_user(database_port, user_form)
            assert True
        except:
            assert False
        mock_get_user_by_username.assert_called_once_with("test_username")


def test_user_validation_invalid_email_success_2(database_port: DatabasePort):
    def fake_get_user_by_username(username):
        return None

    user_form = UserCreationForm(
        **{
            "username": "test_username",
            "email": "valid@anything.com.br",
            "password": "123abcde_?()",
            "password_confirmation": "123abcde_?()",
        }
    )

    with patch.object(
        database_port,
        "get_user_by_username",
        MagicMock(side_effect=fake_get_user_by_username),
    ) as mock_get_user_by_username:
        try:
            _validate_new_user(database_port, user_form)
            assert True
        except:
            assert False


def test_user_validation_invalid_email_success_3(database_port: DatabasePort):
    def fake_get_user_by_username(username):
        return None

    user_form = UserCreationForm(
        **{
            "username": "test_username",
            "email": "val_i.d@anything.com.br",
            "password": "123abcde_?()",
            "password_confirmation": "123abcde_?()",
        }
    )

    with patch.object(
        database_port,
        "get_user_by_username",
        MagicMock(side_effect=fake_get_user_by_username),
    ) as mock_get_user_by_username:
        try:
            _validate_new_user(database_port, user_form)
            assert True
        except:
            assert False


def test_user_validation_different_passwords_exception(database_port: DatabasePort):
    def fake_get_user_by_username(username):
        return None

    user_form = UserCreationForm(
        **{
            "username": "test_username",
            "email": "valid@gmail.com",
            "password": "123abcde_?()",
            "password_confirmation": "123abcde_?((",
        }
    )

    with patch.object(
        database_port,
        "get_user_by_username",
        MagicMock(side_effect=fake_get_user_by_username),
    ) as mock_get_user_by_username:

        try:
            _validate_new_user(database_port, user_form)
            assert False
        except LogicException as e:
            assert True
            expected_exception = LogicException(
                "password and password confirmation don't match",
                status.HTTP_400_BAD_REQUEST,
            )
            assert e.message == expected_exception.message
            assert e.error_status == expected_exception.error_status
        mock_get_user_by_username.assert_not_called()


def test_user_validation_pre_existent_username_exception(database_port: DatabasePort):
    def fake_get_user_by_username(username):
        return User(
            **{"id": "fake_id", "username": "test_username", "email": "valid@gmail.com"}
        )

    user_form = UserCreationForm(
        **{
            "username": "test_username",
            "email": "valid@gmail.com",
            "password": "123abcde_?()",
            "password_confirmation": "123abcde_?()",
        }
    )

    with patch.object(
        database_port,
        "get_user_by_username",
        MagicMock(side_effect=fake_get_user_by_username),
    ) as mock_get_user_by_username:
        try:
            _validate_new_user(database_port, user_form)
            assert False
        except LogicException as e:
            assert True
            expected_exception = LogicException(
                "username is already registered",
                status.HTTP_400_BAD_REQUEST,
            )
            assert e.message == expected_exception.message
            assert e.error_status == expected_exception.error_status
        mock_get_user_by_username.assert_called_once_with(user_form.username)


def test_user_validation_invalid_email_exception_1(database_port: DatabasePort):
    def fake_get_user_by_username(username):
        return None

    user_form = UserCreationForm(
        **{
            "username": "test_username",
            "email": "invalidgmail.com",
            "password": "123abcde_?()",
            "password_confirmation": "123abcde_?()",
        }
    )

    with patch.object(
        database_port,
        "get_user_by_username",
        MagicMock(side_effect=fake_get_user_by_username),
    ) as mock_get_user_by_username:
        try:
            _validate_new_user(database_port, user_form)
            assert False
        except LogicException as e:
            assert True
            expected_exception = LogicException(
                "email format is invalid",
                status.HTTP_400_BAD_REQUEST,
            )

            assert e.message == expected_exception.message
            assert e.error_status == expected_exception.error_status


def test_user_validation_invalid_email_exception_2(database_port: DatabasePort):
    def fake_get_user_by_username(username):
        return None

    user_form = UserCreationForm(
        **{
            "username": "test_username",
            "email": "invalid@gmailcom",
            "password": "123abcde_?()",
            "password_confirmation": "123abcde_?()",
        }
    )

    with patch.object(
        database_port,
        "get_user_by_username",
        MagicMock(side_effect=fake_get_user_by_username),
    ) as mock_get_user_by_username:
        try:
            _validate_new_user(database_port, user_form)
            assert False
        except LogicException as e:
            assert True
            expected_exception = LogicException(
                "email format is invalid",
                status.HTTP_400_BAD_REQUEST,
            )

            assert e.message == expected_exception.message
            assert e.error_status == expected_exception.error_status


def test_user_validation_invalid_email_exception_3(database_port: DatabasePort):
    def fake_get_user_by_username(username):
        return None

    user_form = UserCreationForm(
        **{
            "username": "test_username",
            "email": "invalid@gma@il.com",
            "password": "123abcde_?()",
            "password_confirmation": "123abcde_?()",
        }
    )

    with patch.object(
        database_port,
        "get_user_by_username",
        MagicMock(side_effect=fake_get_user_by_username),
    ) as mock_get_user_by_username:
        try:
            _validate_new_user(database_port, user_form)
            assert False
        except LogicException as e:
            assert True
            expected_exception = LogicException(
                "email format is invalid",
                status.HTTP_400_BAD_REQUEST,
            )

            assert e.message == expected_exception.message
            assert e.error_status == expected_exception.error_status
