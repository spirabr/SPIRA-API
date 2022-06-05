from pymongo import MongoClient
from typing import Union
from bson import ObjectId
import configparser

from domain.interfaces.database_interface import DatabaseInterface
from domain.model.user import User
from adapters.database.service.helpers import user_helper

cfg = configparser.ConfigParser()
cfg.read("adapters/database/.cfg")


class MongoAdapter(DatabaseInterface):
    def __init__(self):
        self._conn = MongoClient(cfg["database"]["conn_url"])
        self._db = getattr(self._conn, cfg["database"]["database_name"])
        self._users = getattr(self._db, cfg["database"]["user_collection_name"])

    def get_user_by_id(self, user_id: str) -> Union[User, None]:
        return user_helper(self._users.find_one({"_id": ObjectId(user_id)}))

    def get_user_by_username(self, username: str) -> Union[User, None]:
        return user_helper(self._users.find_one({"username": username}))
