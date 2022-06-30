import pytest
from unittest.mock import MagicMock, patch
from core.model.user import UserCreationForm
from core.ports.database_port import DatabasePort

from core.services.user_service import _validate_new_user
from tests.mocks.mongo_mock import MongoMock


adapter_instance = MongoMock()


@pytest.fixture()
def database_port():
    port = DatabasePort(adapter_instance)
    return port


def test_user_validation_success(database_port: DatabasePort):
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
        adapter_instance,
        "get_user_by_username",
        MagicMock(side_effect=fake_get_user_by_username),
    ) as mock_get_user_by_username:

        try:
            _validate_new_user(database_port, user_form)
            assert True
        except Exception as e:
            print(e)
            assert False
        mock_get_user_by_username.assert_called_once_with("test_username")
