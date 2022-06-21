from unittest import mock
from unittest.mock import MagicMock, patch, ANY
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from core.model.exception import LogicException
from core.model.token import Token
from core.model.user import User, UserCreationForm

from src.app import create_app

from tests.integration_tests.config import (
    configure_ports_without_auth,
    configure_ports_with_auth,
)


@pytest.fixture()
def client_with_auth():
    ports = configure_ports_with_auth()
    app = create_app(ports)
    yield TestClient(app)


@pytest.fixture()
def client_without_auth():
    app = create_app(configure_ports_without_auth())
    yield TestClient(app)


def test_get_user_by_id_success(client_with_auth: TestClient):
    with patch("adapters.routers.v1.user_router.get_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = User(
            id="507f1f77bcf86cd799439011",
            username="test_username2",
            email="test_email2",
        )
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/users/507f1f77bcf86cd799439011", headers=headers
        )

        mock_get_by_id.assert_called_once_with(
            ANY,
            ANY,
            "507f1f77bcf86cd799439011",
            Token(content="mock_token"),
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": "507f1f77bcf86cd799439011",
            "username": "test_username2",
            "email": "test_email2",
        }


def test_get_user_by_id_exception(client_with_auth: TestClient):
    with patch("adapters.routers.v1.user_router.get_by_id") as mock_get_by_id_failed:
        mock_get_by_id_failed.side_effect = LogicException(
            "user id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get("/v1/users/invalid_id", headers=headers)

        mock_get_by_id_failed.assert_called_once_with(
            ANY,
            ANY,
            "invalid_id",
            Token(content="mock_token"),
        )
        assert response.status_code == 422
        assert response.json() == {"detail": "user id is not valid"}


def test_post_create_user_success(client_with_auth: TestClient):
    with patch("adapters.routers.v1.user_router.create_new_user") as mock_create_user:
        fake_user = {
            "username": "teste",
            "email": "teste@gmail.com",
            "password": "abcde",
            "password_confirmation": "abcde",
        }
        response = client_with_auth.post(
            "/v1/users/",
            headers={
                "Authorization": "Bearer mock_token",
                "Content-Type": "application/json",
            },
            json=fake_user,
        )
        mock_create_user.assert_called_once_with(
            ANY,
            ANY,
            UserCreationForm(
                **{
                    "username": "teste",
                    "email": "teste@gmail.com",
                    "password": "abcde",
                    "password_confirmation": "abcde",
                }
            ),
            Token(content="mock_token"),
        )
        assert response.status_code == 200
        assert response.json() == {"message": "user registered!"}


def test_post_create_user_exception(client_with_auth: TestClient):
    with patch("adapters.routers.v1.user_router.create_new_user") as mock_create_user:
        mock_create_user.side_effect = LogicException(
            "cound not create new user", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        fake_user = {
            "username": "teste",
            "email": "teste@gmail.com",
            "password": "abcde",
            "password_confirmation": "abcde",
        }
        response = client_with_auth.post(
            "/v1/users/",
            headers={
                "Authorization": "Bearer mock_token",
                "Content-Type": "application/json",
            },
            json=fake_user,
        )

        mock_create_user.assert_called_once_with(
            ANY,
            ANY,
            UserCreationForm(
                **{
                    "username": "teste",
                    "email": "teste@gmail.com",
                    "password": "abcde",
                    "password_confirmation": "abcde",
                }
            ),
            Token(content="mock_token"),
        )
        assert response.status_code == 500
        assert response.json() == {"detail": "cound not create new user"}


# tests without authentication


def test_get_user_by_id_no_token_header(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/users/507f1f77bcf86cd799439021")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_post_create_user_no_token_header(client_without_auth: TestClient):
    fake_user = {
        "username": "teste",
        "email": "teste@gmail.com",
        "password": "abcde",
        "password_confirmation": "abcde",
    }
    response = client_without_auth.post(
        "/v1/users/",
        headers={
            "Content-Type": "application/json",
        },
        json=fake_user,
    )
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
