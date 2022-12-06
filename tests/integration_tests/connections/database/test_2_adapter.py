import pytest
from bson import ObjectId
import datetime
from adapters.database.mongo_adapter import MongoAdapter
from core.model.inference import InferenceCreation
from core.model.result import ResultCreation, ResultUpdate
from core.model.user import UserCreation
from pymongo import MongoClient

from src.settings import Settings
from tests.mocks.constants import Constants


@pytest.fixture()
def database_adapter():
    try:
        conn = MongoClient(Settings.database_settings.M_CONN_URL)
        conn.drop_database("test_database")
    finally:
        pass

    adapter = MongoAdapter(
        Settings.database_settings.M_CONN_URL,
        "test_database",
        Settings.database_settings.user_collection_name,
        Settings.database_settings.inference_collection_name,
        Settings.database_settings.model_collection_name,
        Settings.database_settings.result_collection_name,
    )

    adapter._users.insert_many(
        [
            {
                "_id": ObjectId("507f191e810c19729de860ea"),
                "username": "test_username",
                "email": "test_email",
                "password": "fake_password",
            },
            {
                "_id": ObjectId("507f1f77bcf86cd799439011"),
                "username": "test_username2",
                "email": "test_email2",
                "password": "fake_password2",
            },
        ]
    )

    adapter._inferences.insert_many(
        [
            Constants.MONGO_INFERENCE_JSON_1,
            Constants.MONGO_INFERENCE_JSON_2,
            Constants.MONGO_INFERENCE_JSON_3,
        ]
    )

    adapter._models.insert_many(
        [
            {
                "_id": ObjectId("629f992d45cda830033cf4cd"),
                "name": "fake_model",
                "publishing_channel": "fake_channel_2",
            },
            {
                "_id": ObjectId("629f994245cda830033cf4cf"),
                "name": "fake_model_2",
                "publishing_channel": "fake_channel_4",
            },
        ]
    )

    adapter._results.insert_one(
        {
            "_id": ObjectId("62abf2cd154f18493d74fcd2"),
            "inference_id": "629f815d6abaa3c5e6cf7c16",
            "output": [0.98765],
            "diagnosis": "positive",
        }
    )

    yield adapter

    adapter._conn.drop_database("test_database")


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

    assert inference == Constants.MONGO_INFERENCE_JSON_1


def test_get_inference_list(database_adapter: MongoAdapter):
    inferences = database_adapter.get_inference_list("507f191e810c19729de860ea")

    assert list(inferences) == [
        Constants.MONGO_INFERENCE_JSON_1,
        Constants.MONGO_INFERENCE_JSON_2,
    ]


def test_insert_inference(database_adapter: MongoAdapter):
    try:
        database_adapter.insert_inference(
            InferenceCreation(
                age=20,
                gender="F",
                rgh="fake_rgh",
                covid_status="Sim",
                local="hospital_1",
                cid="fake_cid",
                bpm="fake_bpm",
                mask_type="None",
                user_id="507f191e810c19729de860ea",
                model_id="629f994245cda830033cf4cf",
                status="processing",
                created_in=str(datetime.datetime.now()),
            )
        )
    except:
        pytest.fail("test_insert_inference failed")


def test_inference_status_update(database_adapter: MongoAdapter):
    try:
        database_adapter.update_inference_status(
            "629f815d6abaa3c5e6cf7c16", "completed"
        )
    except:
        pytest.fail("test_update_inference_status failed")
    updated_inference = database_adapter.get_inference_by_id(
        "629f815d6abaa3c5e6cf7c16", "507f191e810c19729de860ea"
    )
    assert updated_inference["status"] == "completed"


def test_get_model_by_id(database_adapter: MongoAdapter):
    model = database_adapter.get_model_by_id("629f992d45cda830033cf4cd")

    assert model == {
        "_id": ObjectId("629f992d45cda830033cf4cd"),
        "name": "fake_model",
        "publishing_channel": "fake_channel_2",
    }


def test_get_model_list(database_adapter: MongoAdapter):
    models = database_adapter.get_model_list()
    assert list(models) == [
        {
            "_id": ObjectId("629f992d45cda830033cf4cd"),
            "name": "fake_model",
            "publishing_channel": "fake_channel_2",
        },
        {
            "_id": ObjectId("629f994245cda830033cf4cf"),
            "name": "fake_model_2",
            "publishing_channel": "fake_channel_4",
        },
    ]


def test_get_result_by_inference_id(database_adapter: MongoAdapter):
    result = database_adapter.get_result_by_inference_id("629f815d6abaa3c5e6cf7c16")
    assert result == {
        "_id": ObjectId("62abf2cd154f18493d74fcd2"),
        "inference_id": "629f815d6abaa3c5e6cf7c16",
        "output": [0.98765],
        "diagnosis": "positive",
    }


def test_insert_result(database_adapter: MongoAdapter):
    try:
        database_adapter.insert_result(
            ResultCreation(
                inference_id="629f815d6abaa3c5e6cf7c16",
                output=[-1],
                diagnosis="not available",
            )
        )
    except:
        pytest.fail("test_insert_result failed")


def test_update_result(database_adapter: MongoAdapter):
    try:
        database_adapter.update_result(
            ResultUpdate(
                inference_id="629f815d6abaa3c5e6cf7c16",
                output=[0.987],
                diagnosis="positive",
            )
        )
    except:
        pytest.fail("test_update_result failed")
