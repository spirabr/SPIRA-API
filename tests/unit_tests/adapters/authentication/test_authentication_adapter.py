from operator import truediv
from typing import Optional
from unittest.mock import ANY, MagicMock, patch
import pytest
from core.model.token import Token, TokenData
from core.model.user import User
from adapters.authentication.authentication_adapter import AuthenticationAdapter
from tests.mocks.authentication_mock import AuthenticationJWTMock, AuthenticationMock


@pytest.fixture()
def authentication_adapter():
    adapter_instance = AuthenticationJWTMock()
    return adapter_instance


def test_validate_token(authentication_adapter: AuthenticationAdapter):

    with patch(
        "adapters.authentication.authentication_adapter.jwt.decode"
    ) as mock_method:
        fake_token = Token(content="fake_content")
        mock_method.return_value = {"username": "fake_username"}
        return_value = authentication_adapter.validate_token(fake_token)
        mock_method.assert_called_once_with("fake_content", ANY, algorithms=ANY)
        assert return_value == True


def test_validate_token_exception(authentication_adapter: AuthenticationAdapter):
    with patch(
        "adapters.authentication.authentication_adapter.jwt.decode"
    ) as mock_method:
        fake_token = Token(content="fake_content")
        mock_method.side_effect = Exception()
        return_value = authentication_adapter.validate_token(fake_token)
        mock_method.assert_called_once_with("fake_content", ANY, algorithms=ANY)
        assert return_value == False


def test_decode_token(authentication_adapter: AuthenticationAdapter):

    with patch(
        "adapters.authentication.authentication_adapter.jwt.decode"
    ) as mock_method:
        fake_token = Token(content="fake_content")
        mock_method.return_value = {"username": "fake_username"}
        return_value = authentication_adapter.decode_token(fake_token)
        mock_method.assert_called_once_with("fake_content", ANY, algorithms=ANY)
        assert return_value == TokenData(username="fake_username")


def test_decode_token_exception(authentication_adapter: AuthenticationAdapter):

    with patch(
        "adapters.authentication.authentication_adapter.jwt.decode"
    ) as mock_method:
        fake_token = Token(content="fake_content")
        mock_method.side_effect = Exception()
        try:
            return_value = authentication_adapter.decode_token(fake_token)
            assert False
        except:
            assert True
        mock_method.assert_called_once_with("fake_content", ANY, algorithms=ANY)


def test_verify_password(authentication_adapter: AuthenticationAdapter):
    def fake_verify_password(plain_password: str, user_password: str) -> bool:
        return True

    def fake_verify_password_failed(plain_password: str, user_password: str) -> bool:
        return False

    with patch.object(
        authentication_adapter._pwd_context,
        "verify",
        MagicMock(side_effect=fake_verify_password),
    ) as mock_method:
        return_value = authentication_adapter.verify_password(
            "fake_plain_password", "fake_user_password"
        )
        mock_method.assert_called_once_with("fake_plain_password", "fake_user_password")
        assert return_value == True

    with patch.object(
        authentication_adapter._pwd_context,
        "verify",
        MagicMock(side_effect=fake_verify_password_failed),
    ) as mock_method:
        return_value = authentication_adapter.verify_password(
            "fake_plain_password", "fake_user_password"
        )
        mock_method.assert_called_once_with("fake_plain_password", "fake_user_password")
        assert return_value == False


def test_get_password_hash(authentication_adapter: AuthenticationAdapter):
    def fake_get_password_hash(plain_password: str) -> str:
        return "fake_hash"

    with patch.object(
        authentication_adapter._pwd_context,
        "hash",
        MagicMock(side_effect=fake_get_password_hash),
    ) as mock_method:
        return_value = authentication_adapter.get_password_hash("fake_plain_password")
        mock_method.assert_called_once_with("fake_plain_password")
        assert return_value == "fake_hash"


def test_generate_token(authentication_adapter: AuthenticationAdapter):
    with patch(
        "adapters.authentication.authentication_adapter.jwt.encode"
    ) as mock_method:
        fake_token_data = TokenData(username="fake_username")
        mock_method.return_value = "fake_content"
        return_value = authentication_adapter.generate_token(fake_token_data)
        mock_method.assert_called_once()
        assert return_value == Token(content="fake_content")
