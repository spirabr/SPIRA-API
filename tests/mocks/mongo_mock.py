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
        self._inferences = self._db.inferences
        self._users.insert_one(
            {
                "_id": ObjectId("507f191e810c19729de860ea"),
                "username": "test_username",
                "email": "test_email",
                "hashed_password": self.pwd_context.hash("fake_password"),
            }
        )
