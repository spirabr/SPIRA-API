import pytest
from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo import MongoClient

from adapters.database.mongo_adapter import MongoAdapter
from src.settings import Settings


@pytest.fixture()
def database_adapter():
    try:
        conn = MongoClient(Settings.database_settings.mongo_conn_url)
        conn.drop_database("test_database")
    finally:
        pass

    adapter = MongoAdapter(
        Settings.database_settings.mongo_conn_url,
        "test_database",
        Settings.database_settings.user_collection_name,
        Settings.database_settings.inference_collection_name,
        Settings.database_settings.model_collection_name,
        Settings.database_settings.result_collection_name,
    )

    yield adapter

    adapter._conn.drop_database("test_database")


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
                {
                    "_id": ObjectId(),
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
                },
                {
                    "_id": ObjectId(),
                    "gender": "F",
                    "age": 32,
                    "rgh": "fake_rgh",
                    "covid_status": "Sim",
                    "mask_type": "None",
                    "user_id": "507f191e810c19729de860ea",
                    "model_id": "629f994245cda830033cf4cf",
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
                },
                {
                    "_id": ObjectId(),
                    "gender": "F",
                    "age": 22,
                    "rgh": "fake_rgh",
                    "covid_status": "Sim",
                    "mask_type": "None",
                    "user_id": "629d34d2663c15eb2ed15494",
                    "model_id": "629f994245cda830033cf4cf",
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
                },
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
