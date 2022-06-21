from operator import truediv
from typing import Optional
from unittest.mock import MagicMock, patch
import pytest
from core.model.token import Token, TokenData
from core.model.user import User
from core.ports.authentication_port import AuthenticationPort
from tests.mocks.authentication_mock import AuthenticationMock

adapter_instance = AuthenticationMock()


@pytest.fixture()
def authentication_port():
    port = AuthenticationPort(adapter_instance)
    return port


def test_validate_token(authentication_port: AuthenticationPort):
    def fake_validate_token(token) -> bool:
        return True

    def fake_invalidate_token(token) -> bool:
        return False

    with patch.object(
        adapter_instance,
        "validate_token",
        MagicMock(side_effect=fake_validate_token),
    ) as mock_method:
        fake_token = Token(content="fake_content")
        return_value = authentication_port.validate_token(fake_token)
        mock_method.assert_called_once_with(fake_token)
        assert return_value == True

    with patch.object(
        adapter_instance,
        "validate_token",
        MagicMock(side_effect=fake_invalidate_token),
    ) as mock_method:
        fake_token = Token(content="fake_content")
        return_value = authentication_port.validate_token(fake_token)
        mock_method.assert_called_once_with(fake_token)
        assert return_value == False


def test_decode_token(authentication_port: AuthenticationPort):
    def fake_decode_token(token) -> TokenData:
        return TokenData(username="fake_username")

    with patch.object(
        adapter_instance,
        "decode_token",
        MagicMock(side_effect=fake_decode_token),
    ) as mock_method:
        fake_token = Token(content="fake_content")
        return_value = authentication_port.decode_token(fake_token)
        mock_method.assert_called_once_with(fake_token)
        assert return_value == TokenData(username="fake_username")


def test_decode_token_exception(authentication_port: AuthenticationPort):
    def fake_decode_token(token) -> TokenData:
        raise

    with patch.object(
        adapter_instance,
        "decode_token",
        MagicMock(side_effect=fake_decode_token),
    ) as mock_method:
        fake_token = Token(content="fake_content")
        try:
            return_value = authentication_port.decode_token(fake_token)
            assert False
        except:
            assert True
        mock_method.assert_called_once_with(fake_token)


def test_verify_password_exception(authentication_port: AuthenticationPort):
    def fake_verify_password(plain_password: str, user_password: str) -> bool:
        return True

    def fake_verify_password_failed(plain_password: str, user_password: str) -> bool:
        return False

    with patch.object(
        adapter_instance,
        "verify_password",
        MagicMock(side_effect=fake_verify_password),
    ) as mock_method:
        return_value = authentication_port.verify_password(
            "fake_plain_password", "fake_user_password"
        )
        mock_method.assert_called_once_with("fake_plain_password", "fake_user_password")
        assert return_value == True

    with patch.object(
        adapter_instance,
        "verify_password",
        MagicMock(side_effect=fake_verify_password_failed),
    ) as mock_method:
        return_value = authentication_port.verify_password(
            "fake_plain_password", "fake_user_password"
        )
        mock_method.assert_called_once_with("fake_plain_password", "fake_user_password")
        assert return_value == False


def test_get_password_hash_exception(authentication_port: AuthenticationPort):
    def fake_get_password_hash(plain_password: str) -> str:
        return "fake_hash"

    with patch.object(
        adapter_instance,
        "get_password_hash",
        MagicMock(side_effect=fake_get_password_hash),
    ) as mock_method:
        return_value = authentication_port.get_password_hash("fake_plain_password")
        mock_method.assert_called_once_with("fake_plain_password")
        assert return_value == "fake_hash"


def test_generate_token(authentication_port: AuthenticationPort):
    def fake_generate_token(token_data) -> Token:
        return Token(content="fake_content")

    with patch.object(
        adapter_instance,
        "generate_token",
        MagicMock(side_effect=fake_generate_token),
    ) as mock_method:
        fake_token_data = TokenData(username="fake_username")
        return_value = authentication_port.generate_token(fake_token_data)
        mock_method.assert_called_once_with(fake_token_data)
        assert return_value == Token(content="fake_content")
