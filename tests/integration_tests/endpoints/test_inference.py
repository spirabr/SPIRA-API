from fastapi.testclient import TestClient
import pytest
from adapters.routers.app import create_app

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


def test_get_inference_by_id_success(client_with_auth: TestClient):
    headers = {"Authorization": "Bearer mock_token"}
    response = client_with_auth.get(
        "/v1/users/507f191e810c19729de860ea/inferences/629f815d6abaa3c5e6cf7c16",
        headers=headers,
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
    fake_inference = {
        "sex": "F",
        "age": 23,
        "rgh": "fake_rgh",
        "covid_status": "Sim",
        "mask_type": "None",
        "model_id": "629f992d45cda830033cf4cd",
    }
    fake_files = {
        "aceite": open("tests/mocks/audio_files/audio4.wav", "rb"),
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
    assert response.json() == {"message": "inference registered!"}
    assert response.status_code == 200


def test_post_create_inference_with_invalid_model_id_exception(
    client_with_auth: TestClient,
):
    fake_inference = {
        "sex": "F",
        "age": 23,
        "rgh": "fake_rgh",
        "covid_status": "Sim",
        "mask_type": "None",
        "model_id": "invalid_id",
    }
    fake_files = {
        "aceite": open("tests/mocks/audio_files/audio4.wav", "rb"),
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
    assert response.status_code == 422
    assert response.json() == {"detail": "model id is not valid"}


def test_post_create_inference_with_inexistent_model_exception(
    client_with_auth: TestClient,
):
    fake_inference = {
        "sex": "F",
        "age": 23,
        "rgh": "fake_rgh",
        "covid_status": "Sim",
        "mask_type": "None",
        "model_id": "507f191e810c19729de860ea",
    }
    fake_files = {
        "aceite": open("tests/mocks/audio_files/audio4.wav", "rb"),
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
    assert response.status_code == 404
    assert response.json() == {"detail": "model not found"}


def test_post_create_inference_for_another_user_exception(client_with_auth: TestClient):
    fake_inference = {
        "sex": "F",
        "age": 23,
        "rgh": "fake_rgh",
        "covid_status": "Sim",
        "mask_type": "None",
        "model_id": "invalid_id",
    }
    fake_files = {
        "aceite": open("tests/mocks/audio_files/audio4.wav", "rb"),
        "vogal_sustentada": open("tests/mocks/audio_files/audio1.wav", "rb"),
        "parlenda_ritmada": open("tests/mocks/audio_files/audio2.wav", "rb"),
        "frase": open("tests/mocks/audio_files/audio3.wav", "rb"),
    }
    response = client_with_auth.post(
        "/v1/users/629d34d2663c15eb2ed15494/inferences",
        headers={
            "Authorization": "Bearer mock_token",
        },
        data=fake_inference,
        files=fake_files,
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
    fake_inference = {
        "sex": "F",
        "age": 23,
        "model_id": "629f992d45cda830033cf4cd",
    }
    fake_files = {
        "aceite": open("tests/mocks/audio_files/audio4.wav", "rb"),
        "vogal_sustentada": open("tests/mocks/audio_files/audio1.wav", "rb"),
        "parlenda_ritmada": open("tests/mocks/audio_files/audio2.wav", "rb"),
        "frase": open("tests/mocks/audio_files/audio3.wav", "rb"),
    }
    response = client_without_auth.post(
        "/v1/users/507f191e810c19729de860ea/inferences",
        headers={
            "Authorization": "Bearer mock_token",
        },
        data=fake_inference,
        files=fake_files,
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
