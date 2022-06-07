from bson.objectid import ObjectId
from mongomock import MongoClient
from passlib.context import CryptContext

from src.adapters.database.mongo import MongoAdapter


class MongoMock(MongoAdapter):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._conn = MongoClient()
        self._db = self._conn.spira_db
        self._users = self._db.users
        self._models = self._db.models

        self._users.insert_one(
            {
                "_id": ObjectId("507f191e810c19729de860ea"),
                "username": "test_username",
                "email": "test_email",
                "hashed_password": self.pwd_context.hash("fake_password"),
            }
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
