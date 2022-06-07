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


def test_get_model_by_id_success(client_with_auth: TestClient):
    response = client_with_auth.get("/v1/models/629f992d45cda830033cf4cd")
    assert response.json() == {
        "id": "629f992d45cda830033cf4cd",
        "name": "fake_model",
        "subscribing_topic": "fake_topic_1",
        "publishing_topic": "fake_topic_2",
    }
    assert response.status_code == 200


def test_get_model_by_id_invalid_id_exception(client_with_auth: TestClient):
    response = client_with_auth.get("/v1/models/invalid_id")
    assert response.status_code == 400
    assert response.json() == {"detail": "model id is not valid"}


def test_get_model_by_id_not_found_exception(client_with_auth: TestClient):
    response = client_with_auth.get("/v1/models/507f1f77bcf86cd799439021")
    assert response.status_code == 404
    assert response.json() == {"detail": "model not found"}


def test_get_model_list_success(client_with_auth: TestClient):
    response = client_with_auth.get("/v1/models")
    assert response.json() == {
        "models": [
            {
                "id": "629f992d45cda830033cf4cd",
                "name": "fake_model",
                "subscribing_topic": "fake_topic_1",
                "publishing_topic": "fake_topic_2",
            },
            {
                "id": "629f994245cda830033cf4cf",
                "name": "fake_model_2",
                "subscribing_topic": "fake_topic_3",
                "publishing_topic": "fake_topic_4",
            },
        ]
    }
    assert response.status_code == 200


# tests without authentication


def test_get_model_by_id_unauthorized(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/models/629f992d45cda830033cf4cd")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_get_inference_list_unauthorized(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/models")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
