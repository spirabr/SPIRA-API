from bson.objectid import ObjectId
from mongomock import MongoClient

from adapters.database.mongo_adapter import MongoAdapter
from tests.mocks.constants import Constants


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
                Constants.MONGO_INFERENCE_JSON_1,
                Constants.MONGO_INFERENCE_JSON_2,
                Constants.MONGO_INFERENCE_JSON_3,
            ]
        )

        self._models.insert_many(
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

        self._results.insert_one(
            {
                "_id": ObjectId("62abf2cd154f18493d74fcd2"),
                "inference_id": "629f815d6abaa3c5e6cf7c16",
                "output": [0.98765],
                "diagnosis": "positive",
            }
        )
