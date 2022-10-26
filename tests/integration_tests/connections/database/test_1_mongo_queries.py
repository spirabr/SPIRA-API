import pytest
from bson.objectid import ObjectId
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
                "receiving_channel": "fake_channel_1",
                "publishing_channel": "fake_channel_2",
            },
            {
                "_id": ObjectId("629d34d2663c15eb2ed15491"),
                "name": "fake_model_2",
                "receiving_channel": "fake_channel_3",
                "publishing_channel": "fake_channel_4",
            },
        ]
    )
    adapter._inferences.insert_many(
        [
            {
                "_id": ObjectId("629d34d2663c15eb2ed15492"),
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
                "_id": ObjectId("629d34d2663c15eb2ed15493"),
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
                "_id": ObjectId("629d34d2663c15eb2ed15494"),
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
    adapter._results.insert_one(
        {
            "_id": ObjectId("629d34d2663c15eb2ed15495"),
            "inference_id": "629f815d6abaa3c5e6cf7c16",
            "output": [0.98765],
            "diagnosis": "positive",
        }
    )

    yield adapter

    adapter._conn.drop_database("test_database")


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
        assert inference == {
            "_id": ObjectId("629d34d2663c15eb2ed15492"),
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
            "receiving_channel": "fake_channel_1",
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
