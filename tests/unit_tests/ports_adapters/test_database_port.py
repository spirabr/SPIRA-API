from unittest.mock import MagicMock, patch
import pytest
from core.model.inference import Inference, InferenceCreation
from core.model.model import Model
from core.model.result import Result, ResultCreation
from core.model.user import User, UserCreation, UserWithPassword

from core.ports.database_port import DatabasePort
from tests.mocks.mongo_mock import MongoMock

adapter_instance = MongoMock()


@pytest.fixture()
def database_port():
    port = DatabasePort(adapter_instance)
    return port


def test_get_user_by_id(database_port: DatabasePort):
    user = database_port.get_user_by_id("507f191e810c19729de860ea")
    assert user == User(
        id="507f191e810c19729de860ea", username="test_username", email="test_email"
    )


def test_get_user_by_username(database_port: DatabasePort):
    user = database_port.get_user_by_username("test_username")
    assert user == User(
        **{
            "id": "507f191e810c19729de860ea",
            "username": "test_username",
            "email": "test_email",
        }
    )


def test_get_user_by_username_with_password(database_port: DatabasePort):
    user = database_port.get_user_by_username_with_password("test_username")
    assert user == UserWithPassword(
        **{
            "id": "507f191e810c19729de860ea",
            "username": "test_username",
            "email": "test_email",
            "password": "fake_password",
        }
    )


def test_insert_user(database_port: DatabasePort):
    def fake_adapter_insert(user):
        pass

    new_user = UserCreation(
        username="test_name",
        email="test_email@gmail.com",
        password="fake_password",
    )

    with patch.object(
        adapter_instance, "insert_user", MagicMock(side_effect=fake_adapter_insert)
    ) as fake_adapter_insert:
        database_port.insert_user(new_user)
        fake_adapter_insert.assert_called_once_with(new_user)


def test_get_inference_by_id(database_port: DatabasePort):
    inference = database_port.get_inference_by_id(
        "629f815d6abaa3c5e6cf7c16", "507f191e810c19729de860ea"
    )

    assert inference == Inference(
        **{
            "id": "629f815d6abaa3c5e6cf7c16",
            "sex": "M",
            "age": 23,
            "user_id": "507f191e810c19729de860ea",
            "model_id": "629f992d45cda830033cf4cd",
            "status": "processing",
        },
    )


def test_get_inference_list(database_port: DatabasePort):
    inferences = database_port.get_inference_list("507f191e810c19729de860ea")

    assert inferences == [
        Inference(
            **{
                "id": "629f815d6abaa3c5e6cf7c16",
                "sex": "M",
                "age": 23,
                "user_id": "507f191e810c19729de860ea",
                "model_id": "629f992d45cda830033cf4cd",
                "status": "processing",
            },
        ),
        Inference(
            **{
                "id": "629f81986abaa3c5e6cf7c17",
                "sex": "F",
                "age": 32,
                "user_id": "507f191e810c19729de860ea",
                "model_id": "629f994245cda830033cf4cf",
                "status": "processing",
            }
        ),
    ]


def test_insert_inference(database_port: DatabasePort):
    def fake_adapter_insert(inference):
        pass

    new_inference = InferenceCreation(
        age=20,
        sex="F",
        user_id="507f191e810c19729de860ea",
        model_id="629f994245cda830033cf4cf",
        status="processing",
    )

    with patch.object(
        adapter_instance, "insert_inference", MagicMock(side_effect=fake_adapter_insert)
    ) as fake_adapter_insert:
        database_port.insert_inference(new_inference)
        fake_adapter_insert.assert_called_once_with(new_inference)


def test_get_model_by_id(database_port: DatabasePort):
    model = database_port.get_model_by_id("629f992d45cda830033cf4cd")

    assert model == Model(
        **{
            "id": "629f992d45cda830033cf4cd",
            "name": "fake_model",
            "subscribing_topic": "fake_topic_1",
            "publishing_topic": "fake_topic_2",
        },
    )


def test_get_model_list(database_port: DatabasePort):
    models = database_port.get_model_list()
    assert models == [
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


def test_get_result_by_inference_id(database_port: DatabasePort):
    result = database_port.get_result_by_inference_id("629f815d6abaa3c5e6cf7c16")
    assert result == Result(
        **{
            "id": "62abf2cd154f18493d74fcd2",
            "inference_id": "629f815d6abaa3c5e6cf7c16",
            "output": 0.98765,
            "diagnosis": "positive",
        }
    )


def test_insert_result(database_port: DatabasePort):
    def fake_adapter_insert(result):
        pass

    new_result = ResultCreation(
        inference_id="629f815d6abaa3c5e6cf7c16", output=-1, diagnosis="not available"
    )
    with patch.object(
        adapter_instance, "insert_result", MagicMock(side_effect=fake_adapter_insert)
    ) as fake_adapter_insert:
        database_port.insert_result(new_result)
        fake_adapter_insert.assert_called_once_with(new_result)
