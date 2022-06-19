from fastapi.testclient import TestClient
import pytest
from adapters.message_service.nats_adapter import NATSAdapter
from core.ports.message_service_port import MessageServicePort

from src.app import create_app
<<<<<<< HEAD:tests/unit_tests/test_user.py
import pytest

from adapters.authentication.authentication_adapter import AuthenticationAdapter
from adapters.database.mongo_adapter import MongoAdapter

from core.ports.authentication_port import AuthenticationPort
from src.core.ports.database_port import DatabasePort

from tests.mocks.authentication_mock import AuthenticationMock
from tests.mocks.mongo_mock import MongoMock


def configure_ports_without_auth():
    ports = {}
    ports["database_port"] = DatabasePort(MongoMock())
    ports["authentication_port"] = AuthenticationPort(AuthenticationAdapter())
    ports["message_service_port"] = MessageServicePort(NATSAdapter())
    return ports


def configure_ports_with_auth():
    ports = {}
    ports["database_port"] = DatabasePort(MongoMock())
    ports["authentication_port"] = AuthenticationPort(AuthenticationMock())
    ports["message_service_port"] = MessageServicePort(NATSAdapter())
    return ports

=======
>>>>>>> main:tests/integration_tests/test_user.py

from tests.integration_tests.config import (
    configure_ports_without_auth,
    configure_ports_with_auth,
)


@pytest.fixture()
def client_with_auth():
    app = create_app(configure_ports_with_auth())
    yield TestClient(app)


@pytest.fixture()
def client_without_auth():
    app = create_app(configure_ports_without_auth())
    yield TestClient(app)


def test_get_user_by_id_success(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/507f1f77bcf86cd799439011", headers=headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "507f1f77bcf86cd799439011",
        "username": "test_username2",
        "email": "test_email2",
    }


def test_get_user_by_id_invalid_id_exception(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get("/v1/users/invalid_id", headers=headers)
    assert response.status_code == 422
    assert response.json() == {"detail": "user id is not valid"}


def test_get_user_by_id_not_found_exception(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/507f1f77bcf86cd799439021", headers=headers
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "user not found"}


def test_post_create_user_success(client_with_auth: TestClient):
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
    assert response.status_code == 200
    assert response.json() == {"message": "user registered!"}


# tests without authentication


def test_get_user_by_id_no_token_heder(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/users/507f1f77bcf86cd799439021")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_get_user_by_id_unauthorized(client_without_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_without_auth.get(
        "/v1/users/507f1f77bcf86cd799439021", headers=headers
    )
    assert response.json() == {"detail": "could not validate the credentials"}
    assert response.status_code == 401


def test_post_create_user_unauthorized(client_without_auth: TestClient):
    fake_user = {
        "username": "teste",
        "email": "teste@gmail.com",
        "password": "abcde",
        "password_confirmation": "abcde",
    }
    response = client_without_auth.post(
        "/v1/users/",
        headers={"Content-Type": "application/json"},
        json=fake_user,
    )
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
