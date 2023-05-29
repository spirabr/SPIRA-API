import pytest
from bson.objectid import ObjectId
from pymongo.collection import Collection
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

    yield adapter

    adapter._conn.drop_database(Settings.database_settings.DATABASE_NAME)


def test_insert_user(database_adapter: MongoAdapter):
    try:
        database_adapter._users.insert_one(
            {
                "_id": ObjectId(),
                "username": "fake_user",
                "email": "fake_email",
                "password": "fake_password",
            },
        )
        assert True
    except:
        assert False


def test_insert_models(database_adapter: MongoAdapter):
    try:
        database_adapter._models.insert_many(
            [
                {
                    "_id": ObjectId(),
                    "name": "fake_model",
                    "publishing_channel": "fake_channel_2",
                },
                {
                    "_id": ObjectId(),
                    "name": "fake_model_2",
                    "publishing_channel": "fake_channel_4",
                },
            ]
        )
        assert True
    except Exception as e:
        print(e, flush=True)
        assert False


def test_insert_inferences(database_adapter: MongoAdapter):
    try:
        database_adapter._inferences.insert_many(
            [
                Constants.MONGO_INFERENCE_JSON_1,
                Constants.MONGO_INFERENCE_JSON_2,
                Constants.MONGO_INFERENCE_JSON_3,
            ]
        )
        assert True
    except:
        assert False


def test_insert_result(database_adapter: MongoAdapter):
    try:
        database_adapter._results.insert_one(
            {
                "_id": ObjectId(),
                "inference_id": "629f815d6abaa3c5e6cf7c16",
                "output": [0.98765],
                "diagnosis": "positive",
            }
        )
        assert True
    except:
        assert False
