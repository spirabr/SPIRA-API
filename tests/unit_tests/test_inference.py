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


def test_get_inference_by_id_success(client_with_auth: TestClient):
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16"
    )
    assert response.json() == {
        "id": "629f815d6abaa3c5e6cf7c16",
        "sex": "M",
        "age": 23,
        "user_id": "507f191e810c19729de860ea",
    }
    assert response.status_code == 200


def test_get_inference_by_id_invalid_id_not_found_exception(
    client_with_auth: TestClient,
):
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/invalid_id"
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "inference id is not valid"}


def test_get_inference_by_id_not_found_exception(client_with_auth: TestClient):
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/507f1f77bcf86cd799439021"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "inference not found"}


def test_get_inference_of_another_user_exception(client_with_auth: TestClient):
    response = client_with_auth.get(
        "/v1/users/629d34d2663c15eb2ed15494/inferences/629e4f781ed5308d4b8212bc"
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden operation"}


def test_post_create_inference_success(client_with_auth: TestClient):
    fake_user = {"sex": "F", "age": 23}
    response = client_with_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        headers={"Content-Type": "application/json"},
        json=fake_user,
    )
    assert response.json() == {"message": "inference registered!"}
    assert response.status_code == 200


def test_post_create_inference_for_another_user_exception(client_with_auth: TestClient):
    fake_inference = {"sex": "F", "age": 23}
    response = client_with_auth.post(
        "/v1/users/629d34d2663c15eb2ed15494/inferences",
        headers={"Content-Type": "application/json"},
        json=fake_inference,
    )
    assert response.json() == {"detail": "Forbidden operation"}
    assert response.status_code == 403


def test_get_inference_list_success(client_with_auth: TestClient):
    response = client_with_auth.get("/v1/users/507f191e810c19729de860ea/inferences/")
    assert response.status_code == 200
    assert response.json() == {
        "inferences": [
            {
                "id": "629f815d6abaa3c5e6cf7c16",
                "sex": "M",
                "age": 23,
                "user_id": "507f191e810c19729de860ea",
            },
            {
                "id": "629f81986abaa3c5e6cf7c17",
                "sex": "F",
                "age": 32,
                "user_id": "507f191e810c19729de860ea",
            },
        ]
    }


def test_get_inference_list_of_another_user_exception(client_with_auth: TestClient):
    response = client_with_auth.get("/v1/users/629d34d2663c15eb2ed15494/inferences/")
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden operation"}


# tests without authentication


def test_get_inference_by_id_unauthorized(client_without_auth: TestClient):
    response = client_without_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16"
    )
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_post_create_inference_unauthorized(client_without_auth: TestClient):
    fake_inference = {"sex": "F", "age": 23}
    response = client_without_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        headers={"Content-Type": "application/json"},
        json=fake_inference,
    )
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_get_inference_list_unauthorized(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/users/507f191e810c19729de860ea/inferences/")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
