from bson.objectid import ObjectId
from mongomock import MongoClient
from passlib.context import CryptContext

<<<<<<< HEAD
from adapters.database.mongo_adapter import MongoAdapter


class MongoMock(MongoAdapter):
=======
from src.core.model.user import User


class MongoMock:
>>>>>>> change/hexagonal-architecture
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._conn = MongoClient()
        self._db = self._conn.spira_db
        self._users = self._db.users
        self._inferences = self._db.inferences
        self._models = self._db.models

<<<<<<< HEAD
        self._users.insert_many(
            [
                {
                    "_id": ObjectId("507f191e810c19729de860ea"),
                    "username": "test_username",
                    "email": "test_email",
                    "hashed_password": "fake_password",
                },
                {
                    "_id": ObjectId("507f1f77bcf86cd799439011"),
                    "username": "test_username2",
                    "email": "test_email2",
                    "hashed_password": "fake_password2",
                },
            ]
        )

        self._inferences.insert_many(
            [
                {
                    "_id": ObjectId("629f815d6abaa3c5e6cf7c16"),
                    "sex": "M",
                    "age": 23,
                    "user_id": "507f191e810c19729de860ea",
                    "model_id": "629f992d45cda830033cf4cd",
                },
                {
                    "_id": ObjectId("629f81986abaa3c5e6cf7c17"),
                    "sex": "F",
                    "age": 32,
                    "user_id": "507f191e810c19729de860ea",
                    "model_id": "629f994245cda830033cf4cf",
                },
                {
                    "_id": ObjectId("629e4f781ed5308d4b8212bc"),
                    "sex": "F",
                    "age": 22,
                    "user_id": "629d34d2663c15eb2ed15494",
                    "model_id": "629f994245cda830033cf4cf",
                },
            ]
        )

        self._models.insert_many(
            [
                {
                    "_id": ObjectId("629f992d45cda830033cf4cd"),
                    "name": "fake_model",
                    "subscribing_topic": "fake_topic_1",
                    "publishing_topic": "fake_topic_2",
                },
                {
                    "_id": ObjectId("629f994245cda830033cf4cf"),
                    "name": "fake_model_2",
                    "subscribing_topic": "fake_topic_3",
                    "publishing_topic": "fake_topic_4",
                },
            ]
        )
=======
    def get_user_by_id(self, user_id: str):
        if user_id == "507f1f77bcf86cd799439011":
            return {
                "_id": ObjectId(user_id),
                "username": "test_username",
                "email": "test_email",
            }
        try:
            ObjectId(user_id)
            return None
        except Exception as e:
            raise e
>>>>>>> change/hexagonal-architecture
