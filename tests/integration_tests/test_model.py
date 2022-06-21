from fastapi.testclient import TestClient
import pytest

from src.app import create_app

from tests.config import (
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


# tests with authentication


def test_get_model_by_id_success(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/models/629f992d45cda830033cf4cd", headers=headers
    )
    assert response.json() == {
        "id": "629f992d45cda830033cf4cd",
        "name": "fake_model",
        "subscribing_topic": "fake_topic_1",
        "publishing_topic": "fake_topic_2",
    }
    assert response.status_code == 200


def test_get_model_by_id_invalid_id_exception(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get("/v1/models/invalid_id", headers=headers)
    assert response.status_code == 422
    assert response.json() == {"detail": "model id is not valid"}


def test_get_model_by_id_not_found_exception(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/models/507f1f77bcf86cd799439021", headers=headers
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "model not found"}


def test_get_model_list_success(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get("/v1/models", headers=headers)
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
    headers = {"Authorization": "Bearer mock_token"}
    response = client_without_auth.get(
        "/v1/models/629f992d45cda830033cf4cd", headers=headers
    )
    assert response.json() == {"detail": "could not validate the credentials"}
    assert response.status_code == 401


def test_get_models_list_unauthorized(client_without_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_without_auth.get("/v1/models", headers=headers)
    assert response.json() == {"detail": "could not validate the credentials"}
    assert response.status_code == 401
