from unittest import mock
from unittest.mock import MagicMock, patch, ANY
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from core.model.exception import LogicException
from core.model.model import Model
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


def test_get_model_by_id_success(client_with_auth: TestClient):
    with patch("adapters.routers.v1.model_router.get_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = Model(
            **{
                "id": "629f992d45cda830033cf4cd",
                "name": "fake_model",
                "subscribing_topic": "fake_topic_1",
                "publishing_topic": "fake_topic_2",
            }
        )
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/models/629f992d45cda830033cf4cd", headers=headers
        )

        mock_get_by_id.assert_called_once_with(
            ANY,
            ANY,
            "629f992d45cda830033cf4cd",
            Token(content="mock_token"),
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": "629f992d45cda830033cf4cd",
            "name": "fake_model",
            "subscribing_topic": "fake_topic_1",
            "publishing_topic": "fake_topic_2",
        }


def test_get_model_by_id_exception(client_with_auth: TestClient):
    with patch("adapters.routers.v1.model_router.get_by_id") as mock_get_by_id_failed:
        mock_get_by_id_failed.side_effect = LogicException(
            "model id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get("/v1/models/invalid_id", headers=headers)

        mock_get_by_id_failed.assert_called_once_with(
            ANY,
            ANY,
            "invalid_id",
            Token(content="mock_token"),
        )
        assert response.status_code == 422
        assert response.json() == {"detail": "model id is not valid"}


def test_get_model_list_success(client_with_auth: TestClient):

    with patch("adapters.routers.v1.model_router.get_list") as mock_get_list:
        mock_get_list.return_value = [
            Model(
                **{
                    "id": "629f992d45cda830033cf4cd",
                    "name": "fake_model",
                    "subscribing_topic": "fake_topic_1",
                    "publishing_topic": "fake_topic_2",
                }
            ),
            Model(
                **{
                    "id": "629f994245cda830033cf4cf",
                    "name": "fake_model_2",
                    "subscribing_topic": "fake_topic_3",
                    "publishing_topic": "fake_topic_4",
                }
            ),
        ]
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/models",
            headers=headers,
        )

        mock_get_list.assert_called_once_with(
            ANY,
            ANY,
            Token(content="mock_token"),
        )
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


def test_get_model_list_exception(client_with_auth: TestClient):
    with patch("adapters.routers.v1.model_router.get_list") as mock_get_list_failed:
        mock_get_list_failed.side_effect = LogicException(
            "Forbidden operation", status.HTTP_403_FORBIDDEN
        )
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/models",
            headers=headers,
        )

        mock_get_list_failed.assert_called_once_with(
            ANY,
            ANY,
            Token(content="mock_token"),
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden operation"}


# tests without authentication


def test_get_model_by_id_no_token_header(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/models/629f992d45cda830033cf4cd")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_get_models_list_no_token_header(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/models")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
