import pytest
from bson.objectid import ObjectId
from pymongo import MongoClient

from adapters.database.mongo_adapter import MongoAdapter
from src.settings import Settings
from tests.mocks.constants import Constants


@pytest.fixture()
def database_adapter():
    try:
        conn = MongoClient(Settings.database_settings.M_CONN_URL)
        conn.drop_database(Settings.database_settings.DATABASE_NAME)
    finally:
        pass

    adapter = MongoAdapter(
        Settings.database_settings.M_CONN_URL,
        Settings.database_settings.DATABASE_NAME,
        Settings.database_settings.user_collection_name,
        Settings.database_settings.inference_collection_name,
        Settings.database_settings.model_collection_name,
        Settings.database_settings.result_collection_name,
    )
    adapter._users.insert_one(
        {
            "_id": ObjectId("629d34d2663c15eb2ed15499"),
            "username": "fake_user",
            "email": "fake_email",
            "password": "fake_password",
        },
    )
    adapter._models.insert_many(
        [
            {
                "_id": ObjectId("629d34d2663c15eb2ed15490"),
                "name": "fake_model",
                "publishing_channel": "fake_channel_2",
            },
            {
                "_id": ObjectId("629d34d2663c15eb2ed15491"),
                "name": "fake_model_2",
                "publishing_channel": "fake_channel_4",
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
    adapter._results.insert_one(
        {
            "_id": ObjectId("629d34d2663c15eb2ed15495"),
            "inference_id": "629f815d6abaa3c5e6cf7c16",
            "output": [0.98765],
            "diagnosis": "positive",
        }
    )

    yield adapter

    adapter._conn.drop_database(Settings.database_settings.DATABASE_NAME)


def test_find_user(database_adapter: MongoAdapter):
    try:
        user = database_adapter._users.find_one(
            {
                "username": "fake_user",
            },
        )
        assert user == {
            "_id": ObjectId("629d34d2663c15eb2ed15499"),
            "username": "fake_user",
            "email": "fake_email",
            "password": "fake_password",
        }

    except:
        assert False


def test_find_inference(database_adapter: MongoAdapter):
    try:
        inference = database_adapter._inferences.find_one(
            {
                "gender": "M",
                "age": 23,
            },
        )
        assert inference == Constants.MONGO_INFERENCE_JSON_1

    except:
        assert False


def test_find_model(database_adapter: MongoAdapter):
    try:
        model = database_adapter._models.find_one(
            {
                "name": "fake_model",
            },
        )
        assert model == {
            "_id": ObjectId("629d34d2663c15eb2ed15490"),
            "name": "fake_model",
            "publishing_channel": "fake_channel_2",
        }
    except:
        assert False


def test_find_result(database_adapter: MongoAdapter):
    try:
        result = database_adapter._results.find_one(
            {
                "inference_id": "629f815d6abaa3c5e6cf7c16",
            },
        )
        assert result == {
            "_id": ObjectId("629d34d2663c15eb2ed15495"),
            "inference_id": "629f815d6abaa3c5e6cf7c16",
            "output": [0.98765],
            "diagnosis": "positive",
        }
    except:
        assert False
