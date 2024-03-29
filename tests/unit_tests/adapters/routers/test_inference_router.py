from unittest import mock
from unittest.mock import MagicMock, patch, ANY
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from core.model.exception import LogicException
from core.model.inference import Inference, InferenceCreationForm
from core.model.result import ResultCreation
from core.model.token import Token
from core.model.user import User, UserCreationForm
from core.ports.database_port import DatabasePort

from adapters.routers.app import create_app
from tests.mocks.constants import Constants

from tests.config import (
    configure_ports_without_auth,
    configure_ports_with_auth,
)
from tests.mocks.mongo_mock import MongoMock
from tests.mocks.constants import Constants

database_port_instance = DatabasePort(MongoMock())


@pytest.fixture()
def client_with_auth():
    ports = configure_ports_with_auth()
    ports.database_port = database_port_instance
    app = create_app(ports)
    yield TestClient(app)


@pytest.fixture()
def client_without_auth():
    app = create_app(configure_ports_without_auth())
    yield TestClient(app)


def test_get_inference_by_id_success(client_with_auth: TestClient):

    with patch("adapters.routers.v1.inference_router.get_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = Inference(**Constants.INFERENCE_JSON_1_WITH_ID)
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16",
            headers=headers,
        )

        mock_get_by_id.assert_called_once_with(
            ANY,
            ANY,
            "629f815d6abaa3c5e6cf7c16",
            "507f191e810c19729de860ea",
            Token(content="mock_token"),
        )
        assert response.json() == Constants.INFERENCE_JSON_1_WITH_ID
        assert response.status_code == 200


def test_get_inference_by_id_exception(client_with_auth: TestClient):
    with patch(
        "adapters.routers.v1.inference_router.get_by_id"
    ) as mock_get_by_id_failed:
        mock_get_by_id_failed.side_effect = LogicException(
            "inference id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/users/507f191e810c19729de860ea/inferences/invalid_id",
            headers=headers,
        )

        mock_get_by_id_failed.assert_called_once_with(
            ANY,
            ANY,
            "invalid_id",
            "507f191e810c19729de860ea",
            Token(content="mock_token"),
        )
        assert response.status_code == 422
        assert response.json() == {"detail": "inference id is not valid"}


def test_get_inference_list_success(client_with_auth: TestClient):

    with patch("adapters.routers.v1.inference_router.get_list") as mock_get_list:
        mock_get_list.return_value = [
            Inference(**Constants.INFERENCE_JSON_1_WITH_ID),
            Inference(**Constants.INFERENCE_JSON_2_WITH_ID),
        ]
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/users/507f191e810c19729de860ea/inferences",
            headers=headers,
        )

        mock_get_list.assert_called_once_with(
            ANY,
            ANY,
            "507f191e810c19729de860ea",
            Token(content="mock_token"),
        )
        assert response.json() == {
            "inferences": [
                Constants.INFERENCE_JSON_1_WITH_ID,
                Constants.INFERENCE_JSON_2_WITH_ID,
            ]
        }
        assert response.status_code == 200


def test_get_inference_list_exception(client_with_auth: TestClient):
    with patch("adapters.routers.v1.inference_router.get_list") as mock_get_list_failed:
        mock_get_list_failed.side_effect = LogicException(
            "Forbidden operation", status.HTTP_403_FORBIDDEN
        )
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/users/507f191e810c19729de860ea/inferences",
            headers=headers,
        )

        mock_get_list_failed.assert_called_once_with(
            ANY,
            ANY,
            "507f191e810c19729de860ea",
            Token(content="mock_token"),
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden operation"}


def test_post_create_inference_and_result_success(client_with_auth: TestClient):
    def fake_insert_result(new_result: ResultCreation):
        pass

    with patch(
        "adapters.routers.v1.inference_router.create_new_inference"
    ) as mock_create_inference, patch.object(
        database_port_instance,
        "insert_result",
        MagicMock(side_effect=fake_insert_result),
    ) as fake_result_insert:
        mock_create_inference.return_value = "fake_inference_id"
        response = client_with_auth.post(
            "/v1/users/507f191e810c19729de860ea/inferences",
            headers={
                "Authorization": "Bearer mock_token",
            },
            data=Constants.INFERENCE_JSON_2,
            files=Constants.INFERENCE_FILES,
        )

        mock_create_inference.assert_called_once_with(
            ANY,
            ANY,
            ANY,
            ANY,
            "507f191e810c19729de860ea",
            ANY,
            ANY,
            Token(content="mock_token"),
        )
        fake_result_insert.assert_called_once_with(
            ResultCreation(
                inference_id="fake_inference_id",
                output=[-1],
                diagnosis="not available",
            )
        )
        assert response.status_code == 200

def test_post_create_inference_without_frase(client_with_auth: TestClient):
    def fake_insert_result(new_result: ResultCreation):
        pass

    with patch(
        "adapters.routers.v1.inference_router.create_new_inference"
    ) as mock_create_inference, patch.object(
        database_port_instance,
        "insert_result",
        MagicMock(side_effect=fake_insert_result),
    ) as fake_result_insert:
        mock_create_inference.return_value = "fake_inference_id"
        response = client_with_auth.post(
            "/v1/users/507f191e810c19729de860ea/inferences",
            headers={
                "Authorization": "Bearer mock_token",
            },
            data=Constants.INFERENCE_JSON_2,
            files=Constants.INFERENCE_FILES_WITHOUT_FRASE,
        )

        mock_create_inference.assert_called_once_with(
            ANY,
            ANY,
            ANY,
            ANY,
            "507f191e810c19729de860ea",
            ANY,
            ANY,
            Token(content="mock_token"),
        )
        fake_result_insert.assert_called_once_with(
            ResultCreation(
                inference_id="fake_inference_id",
                output=[-1],
                diagnosis="not available",
            )
        )
        assert response.status_code == 200



# tests without authentication


def test_get_inference_by_id_no_token_header(client_without_auth: TestClient):
    response = client_without_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16"
    )
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_post_create_inference_no_token_header(client_without_auth: TestClient):
    response = client_without_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        data=Constants.INFERENCE_JSON_2,
        files=Constants.INFERENCE_FILES,
    )
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_get_inference_list_no_token_header(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/users/507f191e810c19729de860ea/inferences/")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
