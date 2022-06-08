from typing import Union
from bson.objectid import ObjectId

from src.domain.model.user import User
from src.domain.interfaces.database_interface import DatabaseInterface


class MongoMock(DatabaseInterface):
    def __init__(self):
        pass

    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        if user_id == "507f1f77bcf86cd799439011":
            return User(id=user_id, username="test_username", email="test_email")
        try:
            ObjectId(user_id)
            return None
        except Exception as e:
            raise e
