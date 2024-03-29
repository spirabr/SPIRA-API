from fastapi.testclient import TestClient
import pytest
from fastapi import status
from unittest.mock import ANY, patch, MagicMock
from core.model.exception import LogicException
from core.model.token import Token

from adapters.routers.app import create_app

from core.ports.database_port import DatabasePort
from core.model.inference import Inference, InferenceCreation
from core.model.result import Result, ResultCreation

from tests.mocks.mongo_mock import MongoMock
from tests.mocks.constants import Constants

from tests.config import (
    configure_ports_without_auth,
    configure_ports_with_auth,
)

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


# tests with authentication


def test_get_result_by_inference_id_success(client_with_auth: TestClient):

    with patch(
        "adapters.routers.v1.result_router.get_inference_result"
    ) as mock_get_by_id:
        mock_get_by_id.return_value = Inference(
            **Constants.INFERENCE_JSON_1_WITH_ID
        ), Result(
            **{
                "id": "62abf2cd154f18493d74fcd2",
                "inference_id": "629f815d6abaa3c5e6cf7c16",
                "output": [0.98765],
                "diagnosis": "positive",
            }
        )
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16/result",
            headers=headers,
        )

        mock_get_by_id.assert_called_once_with(
            ANY,
            ANY,
            "629f815d6abaa3c5e6cf7c16",
            "507f191e810c19729de860ea",
            Token(content="mock_token"),
        )
        assert sorted(response.json()) == sorted(
            {
                "inference": Constants.INFERENCE_JSON_1_WITH_ID,
                "result": {
                    "id": "62abf2cd154f18493d74fcd2",
                    "inference_id": "629f815d6abaa3c5e6cf7c16",
                    "output": [0.98765],
                    "diagnosis": "positive",
                },
            }
        )
        assert response.status_code == 200


def test_get_result_by_inference_id_exception(client_with_auth: TestClient):
    with patch(
        "adapters.routers.v1.result_router.get_inference_result"
    ) as mock_get_by_id_failed:
        mock_get_by_id_failed.side_effect = LogicException(
            "inference id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        headers = {"Authorization": "Bearer mock_token"}
        response = client_with_auth.get(
            "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16/result",
            headers=headers,
        )

        mock_get_by_id_failed.assert_called_once_with(
            ANY,
            ANY,
            "629f815d6abaa3c5e6cf7c16",
            "507f191e810c19729de860ea",
            Token(content="mock_token"),
        )
        assert response.status_code == 422
        assert sorted(response.json()) == sorted(
            {"detail": "inference id is not valid"}
        )


# tests without authentication


def test_get_result_by_inference_no_token_header(client_without_auth: TestClient):
    response = client_without_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16/result"
    )
    assert sorted(response.json()) == sorted({"detail": "Not authenticated"})
    assert response.status_code == 401
