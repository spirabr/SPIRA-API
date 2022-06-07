from fastapi.testclient import TestClient
import pytest
from src.app import create_app
import inject

from tests.unit_tests.test_configuration import (
    config_with_auth,
    config_without_auth,
    inject_dependencies,
)

# mock of an authenticated client
@pytest.fixture()
def client_with_auth():
    inject.clear_and_configure(config_with_auth)
    client = TestClient(create_app())
    return client


# mock of a non-authenticated client
@pytest.fixture()
def client_without_auth():
    inject.clear_and_configure(config_without_auth)
    inject_dependencies()
    client = TestClient(create_app())
    return client


# tests with authentication


def test_get_user_by_id_success(client_with_auth: TestClient):
    response = client_with_auth.get("/v1/users/507f191e810c19729de860ea")
    assert response.json() == {
        "id": "507f191e810c19729de860ea",
        "email": "test_email",
        "username": "test_username",
    }
    assert response.status_code == 200


def test_get_user_by_id_invalid_id_exception(client_with_auth: TestClient):
    response = client_with_auth.get("/v1/users/invalid_id")
    assert response.status_code == 400
    assert response.json() == {"detail": "user id is not valid"}


def test_get_user_by_id_not_found_exception(client_with_auth: TestClient):
    response = client_with_auth.get("/v1/users/507f1f77bcf86cd799439021")
    assert response.status_code == 404
    assert response.json() == {"detail": "user not found"}


def test_post_create_user_success(client_with_auth: TestClient):
    fake_user = {"username": "teste", "email": "teste@gmail.com", "password": "abcde"}
    response = client_with_auth.post(
        "/v1/users/",
        headers={"Content-Type": "application/json"},
        json=fake_user,
    )
    assert response.json() == {"message": "user registered!"}
    assert response.status_code == 200


# tests without authentication


def test_get_user_by_id_unauthorized(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/users/507f1f77bcf86cd799439021")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_post_create_user_unauthorized(client_without_auth: TestClient):
    fake_user = {"username": "teste", "email": "teste@gmail.com", "password": "abcde"}
    response = client_without_auth.post(
        "/v1/users/",
        headers={"Content-Type": "application/json"},
        json=fake_user,
    )
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
