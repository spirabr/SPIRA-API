from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock

from src.app import create_app

from core.ports.database_port import DatabasePort
from core.model.inference import InferenceCreation
from core.model.result import ResultCreation

from tests.mocks.mongo_mock import MongoMock

from tests.integration_tests.config import (
    configure_ports_without_auth,
    configure_ports_with_auth,
)

database_port_instance = DatabasePort(MongoMock())


@pytest.fixture()
def client_with_auth():
    ports = configure_ports_with_auth()
    ports["database_port"] = database_port_instance
    app = create_app(ports)
    yield TestClient(app)


@pytest.fixture()
def client_without_auth():
    app = create_app(configure_ports_without_auth())
    yield TestClient(app)


# tests with authentication


def test_get_result_by_inference_id_success(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16/result",
        headers=headers,
    )
    assert response.json() == {
        "inference": {
            "id": "629f815d6abaa3c5e6cf7c16",
            "sex": "M",
            "age": 23,
            "user_id": "507f191e810c19729de860ea",
            "model_id": "629f992d45cda830033cf4cd",
            "status": "processing",
        },
        "result": {
            "id": "62abf2cd154f18493d74fcd2",
            "inference_id": "629f815d6abaa3c5e6cf7c16",
            "output": 0.98765,
            "diagnosis": "positive",
        },
    }
    assert response.status_code == 200


def test_post_create_result_with_inference_success(client_with_auth: TestClient):

    # defining mock calls to port database
    def fake_insert_result(new_result: ResultCreation):
        pass

    def fake_insert_inference(new_inference: InferenceCreation):
        return "fake_inference_id"

    # injecting mocks
    with patch.object(
        database_port_instance,
        "insert_inference",
        MagicMock(side_effect=fake_insert_inference),
    ), patch.object(
        database_port_instance,
        "insert_result",
        MagicMock(side_effect=fake_insert_result),
    ) as fake_result_insert:

        fake_inference = {
            "sex": "F",
            "age": 23,
            "model_id": "629f992d45cda830033cf4cd",
        }

        response = client_with_auth.post(
            "/v1/users/507f191e810c19729de860ea/inferences",
            headers={
                "Authorization": "Bearer mock_token",
                "Content-Type": "application/json",
            },
            json=fake_inference,
        )

        fake_result_insert.assert_called_once_with(
            ResultCreation(
                inference_id="fake_inference_id",
                output=-1,
                diagnosis="not available",
            )
        )
        assert response.json() == {"message": "inference registered!"}
        assert response.status_code == 200
