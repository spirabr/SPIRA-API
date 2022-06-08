from pymongo import MongoClient
from typing import Union
from bson import ObjectId
import configparser

cfg = configparser.ConfigParser()
cfg.read("adapters/database/.cfg")


class MongoAdapter:
    def __init__(self):
        self._conn = MongoClient(cfg["database"]["conn_url"])
        self._db = getattr(self._conn, cfg["database"]["database_name"])
        self._users = getattr(self._db, cfg["database"]["user_collection_name"])

    def get_user_by_id(self, user_id: str):
        return self._users.find_one({"_id": ObjectId(user_id)})
