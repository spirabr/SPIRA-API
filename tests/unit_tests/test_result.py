from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock
from adapters.message_service.nats_adapter import NATSAdapter
from core.model.inference import InferenceCreation
from core.model.result import ResultCreation
from core.ports.message_service_port import MessageServicePort

from src.app import create_app

from adapters.authentication.authentication_adapter import AuthenticationAdapter
from adapters.database.mongo_adapter import MongoAdapter

from core.ports.authentication_port import AuthenticationPort
from src.core.ports.database_port import DatabasePort

from tests.mocks.authentication_mock import AuthenticationMock
from tests.mocks.mongo_mock import MongoMock


database_port_instance = DatabasePort(MongoMock())


def configure_ports_without_auth():
    ports = {}
    ports["database_port"] = DatabasePort(MongoMock())
    ports["authentication_port"] = AuthenticationPort(AuthenticationAdapter())
    ports["message_service_port"] = MessageServicePort(NATSAdapter())
    return ports


def configure_ports_with_auth():
    ports = {}
    ports["database_port"] = database_port_instance
    ports["authentication_port"] = AuthenticationPort(AuthenticationMock())
    ports["message_service_port"] = MessageServicePort(NATSAdapter())
    return ports


@pytest.fixture()
def client_with_auth():
    app = create_app(configure_ports_with_auth())
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
