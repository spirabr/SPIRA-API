from bson.objectid import ObjectId
from mongomock import MongoClient

from adapters.database.mongo_adapter import MongoAdapter


class MongoMock(MongoAdapter):
    def __init__(self):
        self._conn = MongoClient()
        self._db = self._conn.spira_db
        self._users = self._db.users
        self._inferences = self._db.inferences
        self._models = self._db.models
        self._results = self._db.results

        self._users.insert_many(
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

        self._inferences.insert_many(
            [
                {
                    "_id": ObjectId("629f815d6abaa3c5e6cf7c16"),
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
                    "_id": ObjectId("629f81986abaa3c5e6cf7c17"),
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
                    "_id": ObjectId("629e4f781ed5308d4b8212bc"),
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

        self._models.insert_many(
            [
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
        )

        self._results.insert_one(
            {
                "_id": ObjectId("62abf2cd154f18493d74fcd2"),
                "inference_id": "629f815d6abaa3c5e6cf7c16",
                "output": [0.98765],
                "diagnosis": "positive",
            }
        )
