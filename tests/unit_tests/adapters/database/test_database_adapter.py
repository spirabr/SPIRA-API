import pytest
from bson import ObjectId
from adapters.database.mongo_adapter import MongoAdapter
from core.model.inference import InferenceCreation
from core.model.result import ResultCreation
from core.model.user import UserCreation
from tests.mocks.mongo_mock import MongoMock


@pytest.fixture()
def database_adapter():

    # MongoMock inherits all methods from MongoAdapter
    # but uses a mocked client with de DB

    adapter = MongoMock()
    return adapter


def test_get_user_by_id(database_adapter: MongoAdapter):
    user = database_adapter.get_user_by_id("507f191e810c19729de860ea")
    assert user == {
        "_id": ObjectId("507f191e810c19729de860ea"),
        "username": "test_username",
        "email": "test_email",
        "password": "fake_password",
    }


def test_get_user_by_username(database_adapter: MongoAdapter):
    user = database_adapter.get_user_by_username("test_username")
    assert user == {
        "_id": ObjectId("507f191e810c19729de860ea"),
        "username": "test_username",
        "email": "test_email",
        "password": "fake_password",
    }


def test_insert_user(database_adapter: MongoAdapter):
    try:
        database_adapter.insert_user(
            UserCreation(
                username="test_name",
                email="test_email@gmail.com",
                password="fake_password",
            )
        )
    except:
        pytest.fail("test_insert_user failed")


def test_get_inference_by_id(database_adapter: MongoAdapter):
    inference = database_adapter.get_inference_by_id(
        "629f815d6abaa3c5e6cf7c16", "507f191e810c19729de860ea"
    )

    assert inference == {
        "_id": ObjectId("629f815d6abaa3c5e6cf7c16"),
        "sex": "M",
        "age": 23,
        "user_id": "507f191e810c19729de860ea",
        "model_id": "629f992d45cda830033cf4cd",
        "status": "processing",
    }


def test_get_inference_list(database_adapter: MongoAdapter):
    inferences = database_adapter.get_inference_list("507f191e810c19729de860ea")

    assert list(inferences) == [
        {
            "_id": ObjectId("629f815d6abaa3c5e6cf7c16"),
            "sex": "M",
            "age": 23,
            "user_id": "507f191e810c19729de860ea",
            "model_id": "629f992d45cda830033cf4cd",
            "status": "processing",
        },
        {
            "_id": ObjectId("629f81986abaa3c5e6cf7c17"),
            "sex": "F",
            "age": 32,
            "user_id": "507f191e810c19729de860ea",
            "model_id": "629f994245cda830033cf4cf",
            "status": "processing",
        },
    ]


def test_insert_inference(database_adapter: MongoAdapter):
    try:
        database_adapter.insert_inference(
            InferenceCreation(
                age=20,
                sex="F",
                user_id="507f191e810c19729de860ea",
                model_id="629f994245cda830033cf4cf",
                status="processing",
            )
        )
    except:
        pytest.fail("test_insert_inference failed")


def test_get_model_by_id(database_adapter: MongoAdapter):
    model = database_adapter.get_model_by_id("629f992d45cda830033cf4cd")

    assert model == {
        "_id": ObjectId("629f992d45cda830033cf4cd"),
        "name": "fake_model",
        "receiving_channel": "fake_channel_1",
        "publishing_channel": "fake_channel_2",
    }


def test_get_model_list(database_adapter: MongoAdapter):
    models = database_adapter.get_model_list()
    assert list(models) == [
        {
            "_id": ObjectId("629f992d45cda830033cf4cd"),
            "name": "fake_model",
            "receiving_channel": "fake_channel_1",
            "publishing_channel": "fake_channel_2",
        },
        {
            "_id": ObjectId("629f994245cda830033cf4cf"),
            "name": "fake_model_2",
            "receiving_channel": "fake_channel_3",
            "publishing_channel": "fake_channel_4",
        },
    ]


def test_get_result_by_inference_id(database_adapter: MongoAdapter):
    result = database_adapter.get_result_by_inference_id("629f815d6abaa3c5e6cf7c16")
    assert result == {
        "_id": ObjectId("62abf2cd154f18493d74fcd2"),
        "inference_id": "629f815d6abaa3c5e6cf7c16",
        "output": 0.98765,
        "diagnosis": "positive",
    }


def test_insert_result(database_adapter: MongoAdapter):
    try:
        database_adapter.insert_result(
            ResultCreation(
                inference_id="629f815d6abaa3c5e6cf7c16",
                output=-1,
                diagnosis="not available",
            )
        )
    except:
        pytest.fail("test_insert_result failed")
