from typing import Union
from bson.objectid import ObjectId

from src.core.model.user import User


class MongoMock:
    def __init__(self):
        pass

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
