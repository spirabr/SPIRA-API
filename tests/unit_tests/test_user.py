from fastapi.testclient import TestClient
from src.app import create_app

from tests.unit_tests.test_configuration import inject_dependencies

inject_dependencies()
client = TestClient(create_app())


def test_get_user_by_id():
    response = client.get("/v1/users/507f1f77bcf86cd799439011")
    assert response.status_code == 200
    assert response.json() == {
        "id": "507f1f77bcf86cd799439011",
        "email": "test_email",
        "username": "test_username",
    }
