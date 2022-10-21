from fastapi.testclient import TestClient
import pytest

from adapters.routers.app import create_app

from core.ports.database_port import DatabasePort

from tests.mocks.mongo_mock import MongoMock

from tests.config import (
    configure_ports_without_auth,
    configure_ports_with_auth,
)

FAKE_INFERENCE_WITH_ID_1 = {
    "id": "629f815d6abaa3c5e6cf7c16",
    "gender": "M",
    "age": 23,
    "rgh": "fake_rgh",
    "covid_status": "Sim",
    "mask_type": "None",
    "user_id": "507f191e810c19729de860ea",
    "model_id": "629f992d45cda830033cf4cd",
    "status": "processing",
    "cid": "fake_cid",
    "bpm": "fake_bpm",
    "created_in": "2022-07-18 17:07:16.954632",
    "respiratory_frequency": "123",
    "respiratory_insufficiency_status": "Sim",
    "location": "h1",
    "last_positive_diagnose_date": "",
    "hospitalized": "TRUE",
    "hospitalization_start": "2022-07-18 17:07:16.954632",
    "hospitalization_end": "2022-07-18 17:07:16.954632",
    "spo2": "123",
}

FAKE_INFERENCE_WITH_ID_2 = {
    "id": "629f81986abaa3c5e6cf7c17",
    "gender": "F",
    "age": 32,
    "rgh": "fake_rgh",
    "cid": "fake_cid",
    "bpm": "fake_bpm",
    "covid_status": "Sim",
    "mask_type": "None",
    "user_id": "507f191e810c19729de860ea",
    "model_id": "629f994245cda830033cf4cf",
    "status": "processing",
    "created_in": "2022-07-18 17:07:16.954632",
    "respiratory_frequency": "123",
    "respiratory_insufficiency_status": "Sim",
    "location": "h1",
    "last_positive_diagnose_date": "",
    "hospitalized": "TRUE",
    "hospitalization_start": "2022-07-18 17:07:16.954632",
    "hospitalization_end": "2022-07-18 17:07:16.954632",
    "spo2": "123",
}

FAKE_INFERENCE = {
    "gender": "F",
    "age": 23,
    "rgh": "fake_rgh",
    "covid_status": "Sim",
    "mask_type": "None",
    "cid": "fake_cid",
    "bpm": "fake_bpm",
    "model_id": "629f992d45cda830033cf4cd",
    "respiratory_frequency": "123",
    "respiratory_insufficiency_status": "Sim",
    "location": "h1",
    "last_positive_diagnose_date": "",
    "hospitalized": "TRUE",
    "hospitalization_start": "2022-07-18 17:07:16.954632",
    "hospitalization_end": "2022-07-18 17:07:16.954632",
    "spo2": "123",
}

FAKE_FILES = {
    "aceite": open("tests/mocks/audio_files/audio4.wav", "rb"),
    "sustentada": open("tests/mocks/audio_files/audio1.wav", "rb"),
    "parlenda": open("tests/mocks/audio_files/audio2.wav", "rb"),
    "frase": open("tests/mocks/audio_files/audio3.wav", "rb"),
}


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
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16/result",
        headers=headers,
    )
    assert response.json() == {
        "inference": FAKE_INFERENCE_WITH_ID_1,
        "result": {
            "id": "62abf2cd154f18493d74fcd2",
            "inference_id": "629f815d6abaa3c5e6cf7c16",
            "output": 0.98765,
            "diagnosis": "positive",
        },
    }
    assert response.status_code == 200


def test_post_create_result_with_inference_success(client_with_auth: TestClient):
    response = client_with_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        headers={
            "Authorization": "Bearer mock_token",
        },
        data=FAKE_INFERENCE,
        files=FAKE_FILES,
    )
    assert response.json() == {"message": "inference registered!"}
    assert response.status_code == 200


# tests without authentication


def test_get_result_by_inference_unauthorized(client_without_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_without_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16/result",
        headers=headers,
    )
    assert response.json() == {"detail": "could not validate the credentials"}
    assert response.status_code == 401
