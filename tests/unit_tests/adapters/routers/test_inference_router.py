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

from tests.config import (
    configure_ports_without_auth,
    configure_ports_with_auth,
)
from tests.mocks.mongo_mock import MongoMock


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
        mock_get_by_id.return_value = Inference(
            **{
                "id": "629f815d6abaa3c5e6cf7c16",
                "sex": "M",
                "age": 23,
                "rgh": "fake_rgh",
                "covid_status": "Sim",
                "mask_type": "None",
                "user_id": "507f191e810c19729de860ea",
                "model_id": "629f992d45cda830033cf4cd",
                "status": "processing",
                "created_in": "2022-07-18 17:07:16.954632",
            }
        )
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
        assert response.json() == {
            "id": "629f815d6abaa3c5e6cf7c16",
            "sex": "M",
            "age": 23,
            "rgh": "fake_rgh",
            "covid_status": "Sim",
            "mask_type": "None",
            "user_id": "507f191e810c19729de860ea",
            "model_id": "629f992d45cda830033cf4cd",
            "status": "processing",
            "created_in": "2022-07-18 17:07:16.954632",
        }
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
            Inference(
                **{
                    "id": "629f815d6abaa3c5e6cf7c16",
                    "sex": "M",
                    "age": 23,
                    "rgh": "fake_rgh",
                    "covid_status": "Sim",
                    "mask_type": "None",
                    "user_id": "507f191e810c19729de860ea",
                    "model_id": "629f992d45cda830033cf4cd",
                    "status": "processing",
                    "created_in": "2022-07-18 17:07:16.954632",
                }
            ),
            Inference(
                **{
                    "id": "629f81986abaa3c5e6cf7c17",
                    "sex": "F",
                    "age": 32,
                    "rgh": "fake_rgh",
                    "covid_status": "Sim",
                    "mask_type": "None",
                    "user_id": "507f191e810c19729de860ea",
                    "model_id": "629f994245cda830033cf4cf",
                    "status": "processing",
                    "created_in": "2022-07-18 17:07:16.954632",
                }
            ),
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
                {
                    "id": "629f815d6abaa3c5e6cf7c16",
                    "sex": "M",
                    "age": 23,
                    "rgh": "fake_rgh",
                    "covid_status": "Sim",
                    "mask_type": "None",
                    "user_id": "507f191e810c19729de860ea",
                    "model_id": "629f992d45cda830033cf4cd",
                    "status": "processing",
                    "created_in": "2022-07-18 17:07:16.954632",
                },
                {
                    "id": "629f81986abaa3c5e6cf7c17",
                    "sex": "F",
                    "age": 32,
                    "rgh": "fake_rgh",
                    "covid_status": "Sim",
                    "mask_type": "None",
                    "user_id": "507f191e810c19729de860ea",
                    "model_id": "629f994245cda830033cf4cf",
                    "status": "processing",
                    "created_in": "2022-07-18 17:07:16.954632",
                },
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

        fake_inference = {
            "sex": "F",
            "age": 23,
            "rgh": "fake_rgh",
            "covid_status": "Sim",
            "mask_type": "None",
            "model_id": "629f992d45cda830033cf4cd",
        }
        fake_files = {
            "vogal_sustentada": open("tests/mocks/audio_files/audio1.wav", "rb"),
            "parlenda_ritmada": open("tests/mocks/audio_files/audio2.wav", "rb"),
            "frase": open("tests/mocks/audio_files/audio3.wav", "rb"),
        }
        response = client_with_auth.post(
            "/v1/users/507f191e810c19729de860ea/inferences",
            headers={
                "Authorization": "Bearer mock_token",
            },
            data=fake_inference,
            files=fake_files,
        )

        mock_create_inference.assert_called_once_with(
            ANY,
            ANY,
            ANY,
            ANY,
            "507f191e810c19729de860ea",
            InferenceCreationForm(
                **{
                    "sex": "F",
                    "age": 23,
                    "rgh": "fake_rgh",
                    "covid_status": "Sim",
                    "mask_type": "None",
                    "model_id": "629f992d45cda830033cf4cd",
                }
            ),
            ANY,
            Token(content="mock_token"),
        )
        fake_result_insert.assert_called_once_with(
            ResultCreation(
                inference_id="fake_inference_id",
                output=-1,
                diagnosis="not available",
            )
        )
        assert response.status_code == 200
        assert response.json() == {"message": "inference registered!"}


def test_post_create_inference_exception(client_with_auth: TestClient):
    with patch(
        "adapters.routers.v1.inference_router.create_new_inference"
    ) as mock_create_inference:
        mock_create_inference.side_effect = LogicException(
            "cound not create new inference", status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        fake_inference = {
            "sex": "F",
            "age": 23,
            "rgh": "fake_rgh",
            "covid_status": "Sim",
            "mask_type": "None",
            "model_id": "629f992d45cda830033cf4cd",
        }
        fake_files = {
            "vogal_sustentada": open("tests/mocks/audio_files/audio1.wav", "rb"),
            "parlenda_ritmada": open("tests/mocks/audio_files/audio2.wav", "rb"),
            "frase": open("tests/mocks/audio_files/audio3.wav", "rb"),
        }
        response = client_with_auth.post(
            "/v1/users/507f191e810c19729de860ea/inferences",
            headers={
                "Authorization": "Bearer mock_token",
            },
            data=fake_inference,
            files=fake_files,
        )

        mock_create_inference.assert_called_once_with(
            ANY,
            ANY,
            ANY,
            ANY,
            "507f191e810c19729de860ea",
            InferenceCreationForm(
                **{
                    "sex": "F",
                    "age": 23,
                    "rgh": "fake_rgh",
                    "covid_status": "Sim",
                    "mask_type": "None",
                    "model_id": "629f992d45cda830033cf4cd",
                }
            ),
            ANY,
            Token(content="mock_token"),
        )
        assert response.status_code == 500
        assert response.json() == {"detail": "cound not create new inference"}


# tests without authentication


def test_get_inference_by_id_no_token_header(client_without_auth: TestClient):
    response = client_without_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16"
    )
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_post_create_inference_no_token_header(client_without_auth: TestClient):
    fake_inference = {
        "sex": "F",
        "age": 23,
        "rgh": "fake_rgh",
        "covid_status": "Sim",
        "mask_type": "None",
        "model_id": "629f992d45cda830033cf4cd",
    }
    fake_files = {
        "vogal_sustentada": open("tests/mocks/audio_files/audio1.wav", "rb"),
        "parlenda_ritmada": open("tests/mocks/audio_files/audio2.wav", "rb"),
        "frase": open("tests/mocks/audio_files/audio3.wav", "rb"),
    }
    response = client_without_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        data=fake_inference,
        files=fake_files,
    )
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401


def test_get_inference_list_no_token_header(client_without_auth: TestClient):
    response = client_without_auth.get("/v1/users/507f191e810c19729de860ea/inferences/")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401
