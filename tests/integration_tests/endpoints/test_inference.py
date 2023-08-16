from fastapi.testclient import TestClient
import pytest
from adapters.routers.app import create_app

from tests.config import (
    configure_ports_without_auth,
    configure_ports_with_auth,
)
from tests.mocks.constants import Constants


@pytest.fixture()
def client_with_auth():
    app = create_app(configure_ports_with_auth())
    yield TestClient(app)


@pytest.fixture()
def client_without_auth():
    app = create_app(configure_ports_without_auth())
    yield TestClient(app)


# tests with authentication


def test_get_inference_by_id_success(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16",
        headers=headers,
    )
    assert response.json() == Constants.INFERENCE_JSON_1_WITH_ID
    assert response.status_code == 200


def test_get_inference_by_id_invalid_id_not_found_exception(
    client_with_auth: TestClient,
):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/invalid_id", headers=headers
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "inference id is not valid"}


def test_get_inference_by_id_not_found_exception(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/507f1f77bcf86cd799439021",
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "inference not found"}


def test_get_inference_of_another_user_exception(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/629d34d2663c15eb2ed15494/inferences/629e4f781ed5308d4b8212bc",
        headers=headers,
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden operation"}


def test_post_create_inference_success(client_with_auth: TestClient):
    response = client_with_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        headers={
            "Authorization": "Bearer mock_token",
        },
        data=Constants.INFERENCE_JSON_2,
        files=Constants.INFERENCE_FILES,
    )
    assert response.status_code == 200


def test_post_create_inference_with_invalid_model_id_exception(
    client_with_auth: TestClient,
):
    response = client_with_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        headers={
            "Authorization": "Bearer mock_token",
        },
        data=Constants.INFERENCE_JSON_2_INVALID_MODEL,
        files=Constants.INFERENCE_FILES,
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "model id is not valid"}


def test_post_create_inference_with_inexistent_model_exception(
    client_with_auth: TestClient,
):
    response = client_with_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        headers={
            "Authorization": "Bearer mock_token",
        },
        data=Constants.INFERENCE_JSON_2_INEXISTENT_MODEL,
        files=Constants.INFERENCE_FILES,
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "model not found"}


def test_post_create_inference_for_another_user_exception(client_with_auth: TestClient):
    response = client_with_auth.post(
        "/v1/users/629d34d2663c15eb2ed15494/inferences",
        headers={
            "Authorization": "Bearer mock_token",
        },
        data=Constants.INFERENCE_JSON_2,
        files=Constants.INFERENCE_FILES,
    )
    assert response.json() == {"detail": "Forbidden operation"}
    assert response.status_code == 403


def test_get_inference_list_success(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/", headers=headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "inferences": [
            Constants.INFERENCE_JSON_1_WITH_ID,
            Constants.INFERENCE_JSON_2_WITH_ID,
        ]
    }


def test_get_inference_list_of_another_user_exception(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/629d34d2663c15eb2ed15494/inferences/", headers=headers
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden operation"}


# tests without authentication


def test_get_inference_by_id_unauthorized(client_without_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_without_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16",
        headers=headers,
    )
    assert response.json() == {"detail": "could not validate the credentials"}
    assert response.status_code == 401


def test_post_create_inference_unauthorized(client_without_auth: TestClient):
    response = client_without_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        headers={
            "Authorization": "Bearer mock_token",
        },
        data=Constants.INFERENCE_JSON_2,
        files=Constants.INFERENCE_FILES,
    )
    assert response.json() == {"detail": "could not validate the credentials"}
    assert response.status_code == 401


def test_get_inference_list_unauthorized(client_without_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_without_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/", headers=headers
    )
    assert response.json() == {"detail": "could not validate the credentials"}
    assert response.status_code == 401
