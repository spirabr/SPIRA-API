from fastapi.testclient import TestClient
from src.app import create_app

from tests.unit_tests.test_configuration import inject_dependencies

inject_dependencies()
client = TestClient(create_app())


def test_get_user_by_id_success():
    response = client.get("/v1/users/507f1f77bcf86cd799439011")
    assert response.status_code == 200
    assert response.json() == {
        "id": "507f1f77bcf86cd799439011",
        "email": "test_email",
        "username": "test_username",
    }


def test_get_user_by_id_invalid_id():
    response = client.get("/v1/users/invalid_id")
    assert response.status_code == 400
    assert response.json() == {"detail": "user id is not valid"}


def test_get_user_by_id_not_found():
    response = client.get("/v1/users/507f1f77bcf86cd799439021")
    assert response.status_code == 404
    assert response.json() == {"detail": "user not found"}
