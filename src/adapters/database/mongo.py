from pymongo import MongoClient
from typing import Union, List
from bson import ObjectId
import configparser

from domain.interfaces.database_interface import DatabaseInterface
from domain.model.user import User, AuthenticationUser
from domain.model.inference import Inference
from adapters.database.service.helpers import (
    user_helper,
    auth_user_helper,
    inference_helper,
)

cfg = configparser.ConfigParser()
cfg.read("adapters/database/.cfg")


class MongoAdapter(DatabaseInterface):
    def __init__(self):
        self._conn = MongoClient(cfg["database"]["conn_url"])
        self._db = getattr(self._conn, cfg["database"]["database_name"])
        self._users = getattr(self._db, cfg["database"]["user_collection_name"])
        self._inferences = getattr(
            self._db, cfg["database"]["inference_collection_name"]
        )

    # user methods

    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        return user_helper(self._users.find_one({"_id": ObjectId(user_id)}))

    def get_auth_user_by_username(
        self, username: str
    ) -> Union[AuthenticationUser, None]:
        return auth_user_helper(self._users.find_one({"username": username}))

    def get_user_by_username(self, username: str) -> Union[User, None]:
        return user_helper(self._users.find_one({"username": username}))

    def insert_user(self, user: AuthenticationUser) -> None:
        self._users.insert_one(user.dict())

    # inference methods

    def get_inference_list_by_user_id(
        self, user_id: str
    ) -> Union[List[Inference], None]:
        return [
            inference_helper(inference)
            for inference in self._inferences.find({"user_id": user_id})
        ]

    def get_inference_by_id(self, inference_id: str) -> Union[Inference, None]:
        return inference_helper(
            self._inferences.find_one({"_id": ObjectId(inference_id)})
        )

    def insert_inference(self, inference: Inference) -> None:
        return self._inferences.insert_one(inference.dict())
